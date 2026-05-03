import os
import json
import threading
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load agents
from agents.news_fetcher import fetch_top_news
from agents.script_writer import write_script
from agents.image_fetcher import fetch_images
from agents.voiceover import generate_voiceover
from agents.background_generator import generate_background_video
from agents.video_assembler import assemble_video
from agents.social_publisher import generate_social_caption, schedule_post, list_pending_posts

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Global state for task tracking
tasks = {}

def run_pipeline(task_id, genre):
    try:
        def update_status(step, details=None):
            tasks[task_id]['status'] = step
            if details:
                tasks[task_id]['logs'].append(details)
            print(f"Task {task_id}: {step} - {details}")

        update_status('fetching_news', 'Connecting to global news APIs...')
        news = fetch_top_news(genre)
        update_status('fetching_news', 'Successfully scraped top trending stories.')
        
        update_status('writing_script', 'Analyzing trends and writing viral script...')
        script = write_script(news, genre)
        update_status('writing_script', 'Viral 60-second script finalized.')
        
        update_status('fetching_images', 'Searching for high-quality portrait assets...')
        images = fetch_images(genre)
        update_status('fetching_images', f'Downloaded {len(images)} optimized images.')
        
        update_status('generating_audio', 'Generating human-like AI voiceover...')
        audio = generate_voiceover(script)
        
        from moviepy.editor import AudioFileClip
        duration = AudioFileClip(audio).duration
        update_status('generating_audio', f'Voiceover complete. Duration: {duration:.1f}s')
        
        update_status('generating_video', 'Synchronizing visuals with audio track...')
        background = generate_background_video(images, duration)
        update_status('generating_video', 'Background sequence ready.')
        
        update_status('assembling', 'Starting final render: Layering text and audio...')
        final_video = assemble_video(script, audio, background)
        update_status('assembling', 'Final export finished.')
        
        update_status('generating_caption', 'Creating captions...')
        caption = generate_social_caption(script)
        
        # Save to history via the social publisher logic
        schedule_post(final_video, caption, "YouTube")
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result'] = {
            'video': f"/{final_video}",
            'caption': caption,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['error'] = str(e)
        tasks[task_id]['logs'].append(f"ERROR: {str(e)}")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/generate', methods=['POST'])
def start_pipeline():
    data = request.json
    genre = data.get('genre', 'Technology')
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'queued', 'genre': genre, 'logs': []}
    
    thread = threading.Thread(target=run_pipeline, args=(task_id, genre))
    thread.start()
    return jsonify({'task_id': task_id})

@app.route('/api/status/<task_id>')
def get_status(task_id):
    return jsonify(tasks.get(task_id, {'status': 'not_found'}))

@app.route('/api/history')
def get_history():
    return jsonify(list_pending_posts())

@app.route('/api/accounts')
def get_accounts():
    accounts = []
    if os.path.exists('credentials/youtube_token.json'):
        accounts.append({'platform': 'YouTube', 'name': 'Connected', 'status': 'connected', 'icon': 'fa-youtube'})
    else:
        accounts.append({'platform': 'YouTube', 'name': 'Not Connected', 'status': 'disconnected', 'icon': 'fa-youtube'})
    
    accounts.append({'platform': 'Instagram', 'name': 'Coming Soon', 'status': 'disconnected', 'icon': 'fa-instagram'})
    return jsonify(accounts)

@app.route('/output/<path:path>')
def serve_output(path):
    return send_from_directory('output', path)

if __name__ == '__main__':
    os.makedirs('output/videos', exist_ok=True)
    os.makedirs('output/audio', exist_ok=True)
    os.makedirs('output/backgrounds', exist_ok=True)
    os.makedirs('output/scheduler', exist_ok=True)
    
    # Render/Railway dynamic port binding
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
