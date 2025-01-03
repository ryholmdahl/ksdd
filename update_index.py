def insert_comment_section(index_path):
    with open(index_path, 'r') as file:
        content = file.read()
    
    # Check if comment section already exists
    if 'id="comment-section"' in content:
        return
    
    # First, add CSS to the head section
    css_styles = '''
    <style>
      #unity-container.unity-desktop {
        margin-bottom: 20px;
      }
      body {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
        margin: 0;
        padding: 20px 0;
      }
      #comment-text:focus {
        z-index: 1000;
      }
    </style>
  </head>'''
    
    content = content.replace('</head>', css_styles)
       
    # Insert script to handle Unity canvas before the existing script
    unity_handler = '''
    <script>
      // Override the default Unity canvas setup
      const originalCreateUnityInstance = window.createUnityInstance;
      window.createUnityInstance = (...args) => {
        return originalCreateUnityInstance(...args).then(instance => {
          const canvas = document.querySelector("#unity-canvas");
          const textarea = document.querySelector("#comment-text");
          
          textarea.addEventListener('focus', () => {
            canvas.style.pointerEvents = 'none';
            canvas.style.display = 'none';
            setTimeout(() => canvas.style.display = 'block', 100);
          });
          
          textarea.addEventListener('blur', () => {
            canvas.style.pointerEvents = 'auto';
          });
          
          return instance;
        });
      };
    </script>
    <script>'''
    
    content = content.replace('<script>', unity_handler, 1)

    
    comment_section = '''
      <div id="comment-section" style="max-width: 960px; width: 100%; margin: 20px auto; padding: 20px;">
        <h3>Leave a Comment</h3>
        <textarea id="comment-text" style="width: 100%; height: 100px; margin-bottom: 10px;" 
                  onfocus="pauseUnityInput()" onblur="resumeUnityInput()"></textarea>
        <button onclick="submitComment()" style="padding: 10px 20px;">Submit Comment</button>
      </div>
      <script>
        let unityInstance = null;
        
        // Store the original createUnityInstance call
        const originalCreateUnityInstance = createUnityInstance;
        createUnityInstance = function(canvas, config, onProgress) {
            return originalCreateUnityInstance(canvas, config, onProgress).then((instance) => {
                unityInstance = instance;
                return instance;
            });
        };

        function pauseUnityInput() {
            if (unityInstance) {
                const canvas = document.querySelector("#unity-canvas");
                canvas.setAttribute('tabindex', '-1');
            }
        }

        function resumeUnityInput() {
            if (unityInstance) {
                const canvas = document.querySelector("#unity-canvas");
                canvas.setAttribute('tabindex', '1');
            }
        }

        function submitComment() {
          const comment = document.getElementById('comment-text').value;
          if (comment.trim() === '') {
            alert('Please enter a comment');
            return;
          }
          const subject = encodeURIComponent('Game Feedback');
          const body = encodeURIComponent(comment);
          window.location.href = `mailto:your.email@example.com?subject=${subject}&body=${body}`;
        }
      </script>
    </body>'''
    
    modified_content = content.replace('</body>', comment_section)
    
    with open(index_path, 'w') as file:
        file.write(modified_content)

if __name__ == '__main__':
    insert_comment_section('index.html')