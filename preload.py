from datetime import datetime
import subprocess

cs_base_color = "#003DA5"
cs_course_number = "CatVPy"
cs_header = cs_course_number
cs_long_name = cs_content_header = "Home"
cs_title = cs_course_number
cs_breadcrumbs_html = ""

cs_markdown_ignore_tags = ("script", "svg", "textarea")

cs_top_menu = [
    {"text": "Home", "link": "COURSE"},
]

csq_python3 = True
csq_python_sandbox = "python"
csq_python_sandbox_type = "python"
csq_python_sandbox_interpreter = "/home/aherrera1721/catsoop/catsoop-env/bin/python3"

try:
    csq_sandbox_options["do_rlimits"] = False
except:
    csq_sandbox_options = {"do_rlimits": False}

cs_default_role = "Guest"
cs_permissions = {"Guest": ["view_all", "submit_all"]}


def cs_post_load(context):
    if "cs_long_name" in context:
        context["cs_content_header"] = context["cs_long_name"]
        context["cs_title"] = "%s | %s" % (context["cs_long_name"], context["cs_title"])
    try:
        loc = os.path.abspath(
            os.path.join(context["cs_data_root"], "courses", *context["cs_path_info"])
        )
        git_info = subprocess.check_output(
            [
                "git",
                "log",
                "--pretty=format:%h %ct",
                "-n1",
                "--",
                "content.catsoop",
                "content.md",
                "content.xml",
                "content.py",
            ],
            cwd=loc,
        )
        h, t = git_info.split()
        t = (
            context["csm_time"]
            .long_timestamp(datetime.fromtimestamp(float(t)))
            .replace(";", " at")
        )
        context["cs_footer"] = (
            "This page was last updated on %s (revision <code>%s</code>).<br/>&nbsp;<br/>"
            % (t, h.decode())
        )
    except:
        pass


def init_vpython():
    html = """
    <link type="text/css" href="https://www.glowscript.org/css/redmond/2.1/jquery-ui.custom.css" rel="stylesheet" />
    <style>
    canvas {
        border-radius: 5px !important;
        width: 100% !important;
        cursor: grab !important;
    }
    .glowscript-canvas-wrapper {
        width: 100% !important;
    }
    .glowscript-graph {
        justify-self: center !important;
    }
    .glowscript button {
        background-color: #000000 !important;
        color: #ffffff !important; 
        font-size: 13.3333px !important;
        display: inline-block !important;
        padding: 6px 12px !important;
        border: 1px solid #000000 !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        padding: 6px 12px !important;
        border: 1px solid #000000 !important;
        border-radius: 4px !important;
        cursor: pointer !important;
    }
    .glowscript button:hover, button:active, button:active:hover{
        color: #ffffff !important;
        background-color: #333333 !important;
        border-color: #000000 !important;
        text-decoration: none !important;
        cursor: pointer !important;
    }
    #print {
        box-sizing: border-box !important;
        background-color: #1e1e1e !important; 
        color: #ffffff !important;
        font-family: monospace !important;
        font-size: 14px !important;
        line-height: 1.4 !important;
        padding: 12px !important;
        border: none !important;
        border-radius: 5px !important;
        resize: vertical !important;
        outline: none !important;
        white-space: pre !important;
        overflow: auto !important;
        width: 100% !important;
    }
    </style>
    <script type="text/javascript">
        window.__vpython_thread = undefined;
        catsoop.check_copy = catsoop.check;
        catsoop.check = function (name) {
            if (window.__vpython_thread === undefined) {
                window.__vpython_thread = 0;
            }
            return catsoop.check_copy(name);
        };
        window.MathJax.Hub = {}
        window.MathJax.Hub.Config = function (args) {
            return;
        }
        window.MathJax.Hub.Configured = function () {
            return;
        }
    </script>
    <script type="text/javascript" src="https://www.glowscript.org/lib/jquery/2.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://www.glowscript.org/lib/jquery/2.1/jquery-ui.custom.min.js"></script>
    <script type="text/javascript" src="https://www.glowscript.org/package/glow.3.2.min.js"></script>
    <script type="text/javascript" src="https://www.glowscript.org/package/RSrun.3.2.min.js"></script>
    """
    print(html)
