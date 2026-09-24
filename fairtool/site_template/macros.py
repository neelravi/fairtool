def define_env(env):
    @env.macro
    def structure_viewer(json_path, height="500px"):
        div_id = json_path.replace("/", "_").replace(".", "_")
        return f'''
<div class="structure-card card" style="width: 100%; max-width: 800px; margin: auto; padding: 0em;">
  <div class="structure-viewer" data-json="{json_path}" style="width: 100%; height: {height};"></div>
</div>
'''
