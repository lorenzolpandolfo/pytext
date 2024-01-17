import os

class GitManager:	
	@staticmethod
	def get_current_branch(current_terminal_directory:str):
		GitManager.__move_to_git_dir(current_terminal_directory)
		current_branch = GitManager.__open_head_file()
		return current_branch.replace("\n", "")

	@staticmethod	
	def __move_to_git_dir(current_terminal_directory:str):
		os.chdir(current_terminal_directory)
		os.chdir(".git")
		
	@staticmethod
	def __open_head_file() -> str:
		with open("HEAD", "r", encoding="utf8") as file:
			content = file.read()
		return content.split("/")[-1]
