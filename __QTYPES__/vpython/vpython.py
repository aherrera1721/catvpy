tutor.qtype_inherit("pythoncode")
checktext = "Run Simulation"
defaults["csq_vpython_pre"] = "\nfrom vpython import *"
defaults["csq_vpython_post"] = ""
defaults["csq_code_pre"] = (
    "\nimport vpython\nvpython.baseObj._view_constructed=True\nfrom vpython import *"
)


def get_previous_submissions(**info):
    previous_submissions = {}
    prefix, step = info["csq_name"].rsplit("_", 1)
    exercise_stats = csm_tutor.compute_page_stats(
        globals(),
        info["cs_user_info"]["username"],
        info["cs_path_info"],
        ["actions", "state", "question_info"],
    )
    exercise_submissions = list(
        filter(lambda x: x["action"] == "submit", exercise_stats["actions"])
    )
    for i in range(1, int(step)):
        prev_name = prefix + "_" + str(i)
        prev_sub = list(filter(lambda x: prev_name in x["names"], exercise_submissions))
        if prev_sub:
            previous_submissions[prev_name] = (
                prev_sub[-1]["submitted"][prev_name]["data"] + "\n\n"
            )
        else:
            previous_submissions[prev_name] = ""
    return previous_submissions

def check_previous_submissions(previous_submissions):
    for value in previous_submissions.values():
        if not value:
            return False
    return True

def inject_previous_submissions(code, previous_submissions):
    for key, value in previous_submissions.items():
        code = code.replace(key, value)
    return code


def handle_check(submissions, **info):
    name = info["csq_name"]
    code = get_code(submissions[name], info)
    if not isinstance(code, str):
        return code

    code = "\n\n".join([info["csq_vpython_pre"], code, info["csq_vpython_post"]])
    
    prev_subs = get_previous_submissions(**info)
    if not check_previous_submissions(prev_subs):
        return "<font color='red'>You must submit your code for all of the previous parts.</font>"
    code = inject_previous_submissions(code, prev_subs)

    prefix, _ = info["csq_name"].rsplit("_", 1)

    format_words = {
        "code": code,
        "name": name,
        "prefix": prefix,
    }

    msg = (
        """
        <div id="response-%(name)s" class="response" style="border: none; width: auto;">
        <script type="text/javascript">
            window.glowscript_compile = undefined;
            
            if (window.__vpython_thread !== undefined) {
              window.__vpython_thread += 1;

              $('[id^="response-%(prefix)s_"]').not('#response-%(name)s').remove();
            
              $.ajax({
                url: 'https://www.glowscript.org/package/RScompiler.3.2.min.js',
                dataType: 'script',
                cache: true,
                crossDomain: true,
              })
                .fail(function (xhr, err, exc) {
                  xhr;
                  console.error(err + ' getting ' + xhr.url + ': ' + exc);
                })
                .done(function () {
                  if (!window.glowscript_compile) {
                    console.error('Failed to load compiler');
                    return;
                  }
  
                  if ($('#glowscript-%(name)s')) {
                      $('#glowscript-%(name)s').remove();
                  }
  
                  var embedScript = window.glowscript_compile(String.raw`%(code)s`, {
                    lang: 'vpython',
                    version: '3.2',
                    run: false,
                  });
  
                  embedScript = ';(function() {' + embedScript + ';$(function(){ window.__context = { glowscript_container: $("#glowscript-%(name)s")}; __main__() })})()';
                  embedScript = embedScript.replace('</', '<\\/');
  
                  var thread = window.__vpython_thread;
                  var stopThread = `
                  if (window.__vpython_thread !== ${thread}) {
                    break;
                  }
                  `;

                  embedScript = embedScript.replace(/\(?\s*await\s*rate\s*\(.*\)\s*\)?;/, (match) => `${match}\n${stopThread}`);
  
                  $('#response-%(name)s').prepend('<div id="glowscript-%(name)s" class="glowscript"></div>');
  
                  $('<script>', {
                      text: embedScript,
                  }).appendTo(`#glowscript-%(name)s`);
                });

            } else {
              $('#response-%(name)s').remove();
            }
        </script>
        <b>Code</b>
        <pre style="overflow-x: auto; white-space: pre; margin-top: 0px;">
          <code id="%(name)s_sim_code" class="lang-python">%(code)s</code>
        </pre>
        <script type="text/javascript">
          // @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt AGPL-v3
          hljs.highlightBlock(document.getElementById("%(name)s_sim_code"));
          // @license-end
        </script>
      </div>
    """
        % format_words
    )
    return msg
