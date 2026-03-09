import os
import argparse
import json
from github import Github

def get_node_id(type_name, value):
    return f"{type_name}-{value}"

def ingest_prs(repo_name: str, token: str = None):
    g = Github(token)
    repo = g.get_repo(repo_name)
    # Sort by updated descending to get the most recent activity
    pulls = repo.get_pulls(state='all', sort='updated', direction='desc')
    
    nodes_dict = {}
    edges = []
    
    # We will fetch up to 50 PRs or until rate limit hits
    MAX_PRS = 50
    count = 0
    
    try:
        for pr in pulls:
            if count >= MAX_PRS:
                break
            count += 1
            
            pr_node_id = get_node_id("PR", pr.number)
            nodes_dict[pr_node_id] = {
                "id": pr_node_id,
                "label": "PullRequest",
                "properties": {"title": pr.title, "number": pr.number, "state": pr.state}
            }
            
            if pr.user:
                user_id = pr.user.login
                # Improve agent detection using GitHub's native user.type
                is_bot = pr.user.type == "Bot" or "[bot]" in user_id.lower() or "agent" in user_id.lower() or user_id.lower() == "claude"
                user_type = "Agent" if is_bot else "Human"
                
                user_node_id = get_node_id("User", user_id)
                
                nodes_dict[user_node_id] = {
                    "id": user_node_id,
                    "label": "User",
                    "properties": {"name": user_id, "type": user_type}
                }
                
                edges.append({
                    "source": user_node_id,
                    "target": pr_node_id,
                    "type": "CREATED_PR"
                })
                
            try:
                # This is the most expensive call, likely to hit rate limits on large PRs
                for file in pr.get_files():
                    file_id = get_node_id("File", file.filename)
                    if file_id not in nodes_dict:
                        nodes_dict[file_id] = {
                            "id": file_id,
                            "label": "File",
                            "properties": {"path": file.filename}
                        }
                    
                    edges.append({
                        "source": pr_node_id,
                        "target": file_id,
                        "type": "MODIFIED_FILE"
                    })
            except Exception as e:
                # Catch rate limit on file iteration but continue processing what we have
                print(f"Warning: Could not fetch files for PR {pr.number}. Rate limit or large PR? Error: {e}")
                if "rate limit" in str(e).lower() or "403" in str(e):
                    print("Rate limit reached while fetching PR files. Stopping further PR processing to preserve partial graph.")
                    break # Stop iterating PRs if we hit rate limit on files
                    
    except Exception as e:
        print(f"Error during repository ingestion: {e}")
        if "404" in str(e):
             print(f"Repository {repo_name} not found or requires authentication.")
        # We still return whatever nodes/edges we managed to parsing before the crash
            
    nodes = list(nodes_dict.values())
    print(f"Ingested {len(nodes)} nodes and {len(edges)} edges.")
    
    output = {
        "nodes": nodes,
        "edges": edges
    }
    
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, required=True, help="Format: owner/repo")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    ingest_prs(args.repo, token)
