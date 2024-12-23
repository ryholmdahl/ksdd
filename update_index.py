def insert_comment_section(index_path):
    with open(index_path, 'r') as file:
        content = file.read()
    
    # Check if comment section already exists
    if 'id="comment-section"' in content:
        return
    
    comment_section = '''
      <div id="comment-section" style="max-width: 960px; margin: 20px auto; padding: 20px;">
        <h3>Leave a Comment</h3>
        <textarea id="comment-text" style="width: 100%; height: 100px; margin-bottom: 10px;"></textarea>
        <button onclick="submitComment()" style="padding: 10px 20px;">Submit Comment</button>
      </div>
      <script>
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