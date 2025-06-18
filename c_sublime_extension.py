import sublime
import sublime_plugin
import os
import subprocess

class CompileWithGccCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_path = self.view.file_name()

        if not file_path:
            sublime.message_dialog("Save the file before compiling.")
            return

        if not file_path.endswith(".c"):
            sublime.message_dialog("Only .c files are supported.")
            return

        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        output_exe = os.path.join(file_dir, "a.out")
        output_txt = os.path.join(file_dir, "gcc_output.txt")

        compile_command = f"gcc \"{file_path}\" -o \"{output_exe}\" > \"{output_txt}\" 2>&1 && \"{output_exe}\" >> \"{output_txt}\""

        try:

            subprocess.Popen([
                "terminator", "-e", f"bash -c '{compile_command}; exec bash'"
            ], cwd=file_dir)

            sublime.set_timeout_async(lambda: self.load_output(output_txt), 5000)

        except Exception as e:
            sublime.message_dialog("Error: " + str(e))

    def load_output(self, output_txt):
        if os.path.exists(output_txt):
            with open(output_txt, "r") as f:
                content = f.read()
                self.show_output(content)
        else:
            sublime.message_dialog("Compilation failed or gcc_output.txt was not created.")

    def show_output(self, content):
        output_view = self.view.window().new_file()
        output_view.set_name("GCC Output")
        output_view.set_scratch(True)
        output_view.run_command("append", {"characters": content})