from dotenv import load_dotenv
from core.services.suno_client import SunoClient
from core.services.gemini_client import GeminiClient
from core.services.image_client import ImageClient
from core.services.youtube_client import YouTubeClient
from core.database.database_manager import DatabaseManager
from core.analytics.collector import AnalyticsCollector
from core.analytics.analyzer import PerformanceAnalyzer
from core.utils.file_manager import FileManager
from core.utils.video_creator import VideoCreator
from core.utils.performance_tracker import PerformanceTracker
import json
import time
import shutil

def create_mock_suno_response(task_id: str) -> dict:
    """Create mock Suno API response for testing"""
    return {
        "taskId": task_id,
        "status": "SUCCESS",
        "data": [
            {
                "id": "mock_track_1",
                "title": "Mock Lo-Fi Track 1",
                "audio_url": "https://example.com/mock_audio_1.mp3",
                "image_url": "https://example.com/mock_image_1.jpg",
                "duration": 180.5,
                "model_name": "mock-v4",
                "prompt": "Mock lyrics prompt"
            },
            {
                "id": "mock_track_2",
                "title": "Mock Lo-Fi Track 2",
                "audio_url": "https://example.com/mock_audio_2.mp3",
                "image_url": "https://example.com/mock_image_2.jpg",
                "duration": 195.2,
                "model_name": "mock-v4",
                "prompt": "Mock lyrics prompt"
            }
        ]
    }

def mock_suno_generation() -> dict:
    """Mock Suno music generation for testing"""
    print("🎵 [MOCK] Siunčiama muzikos generavimo užduotis į Suno...")
    task_id = f"mock_task_{int(time.time())}"
    print(f"✅ [MOCK] Užduotis sėkmingai pateikta Suno. Task ID: {task_id}")
    return {"taskId": task_id}

def mock_wait_for_completion(task_id: str) -> dict:
    """Mock waiting for task completion"""
    print(f"🔄 [MOCK] Laukiama užduoties {task_id} užbaigimo...")
    time.sleep(2)  # Simulate waiting
    print("📊 [MOCK] Užduoties būsena: SUCCESS")
    print("✅ [MOCK] Užduotis sėkmingai užbaigta!")
    return create_mock_suno_response(task_id)

def test_youtube_connection():
    """Test YouTube API connection and authentication"""
    print("🎥 Testuojamas YouTube API prisijungimas...")
    print("=" * 50)

    try:
        # Initialize YouTube client (this will handle authentication)
        print("🔐 Inicijuojamas YouTube klientas...")
        youtube = YouTubeClient()

        # Test by getting channel statistics
        print("\n📊 Gaunamos kanalo statistikos...")
        channel_stats = youtube.get_channel_statistics()

        if channel_stats:
            print("\n✅ YouTube API veikia sėkmingai!")
            print("=" * 40)
            print(f"📺 Kanalas: {channel_stats['channel_title']}")
            print(f"🆔 Channel ID: {channel_stats['channel_id']}")
            print(f"👥 Prenumeratoriai: {channel_stats['subscriber_count']:,}")
            print(f"🎬 Video skaičius: {channel_stats['video_count']:,}")
            print(f"👁️  Peržiūros: {channel_stats['view_count']:,}")
            print(f"📝 Aprašymas: {channel_stats['description']}")
            print("=" * 40)

            return {
                'success': True,
                'channel_stats': channel_stats
            }
        else:
            print("❌ Nepavyko gauti kanalo statistikų")
            return {
                'success': False,
                'error': 'Failed to get channel statistics'
            }

    except Exception as e:
        print(f"❌ YouTube testavimo klaida: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def run_creation_pipeline(use_real_apis: bool = False, use_hybrid: bool = False):
    """Main orchestration function for the music creation pipeline"""
    print("🚀 Pradedama autonominio muzikanto sistema...")
    print("=" * 50)

    # Initialize performance tracker
    tracker = PerformanceTracker()

    # Initialize components
    load_dotenv()

    if use_real_apis:
        print("🔑 Naudojami REALŪS API raktai")
        suno = SunoClient()
        gemini = GeminiClient()
        image_client = ImageClient()
    elif use_hybrid:
        print("🔄 HIBRIDINIS REŽIMAS: Realus vaizdas + Mock garsas")
        suno = None
        gemini = GeminiClient()  # Real Gemini for prompts
        image_client = ImageClient()  # Real image generation
    else:
        print("🧪 Naudojami MOCK duomenys (testavimui)")
        suno = None
        gemini = None
        image_client = None

    file_manager = FileManager()
    video_creator = VideoCreator()

    try:
        # Step 1: Check credits (only for real APIs)
        if use_real_apis and suno:
            credits = suno.get_credits()
            print(f"✅ Suno kreditų likutis: {credits}")
            if credits < 10:
                print("⚠️ ĮSPĖJIMAS: Mažai kreditų likę!")
        else:
            print("✅ [MOCK] Kreditų tikrinimas praleistas")

        # Step 2: Generate creative brief
        print("\n🧠 1/5 Generuojama kūrybinė idėja...")
        tracker.start_timer("gemini_brief_generation")

        if use_real_apis and gemini:
            brief = gemini.generate_creative_brief(
                genre="Lo-Fi Hip Hop",
                theme="rainy night in Tokyo"
            )
        elif use_hybrid and gemini:
            brief = gemini.generate_creative_brief(
                genre="Lo-Fi Hip Hop",
                theme="rainy night in Tokyo"
            )
        else:
            # Mock creative brief
            brief = {
                "title": "Midnight Rain Sessions",
                "lyrics_prompt": "Create a lo-fi hip hop track about walking through rainy Tokyo streets at midnight, with neon lights reflecting on wet pavement, feeling nostalgic and peaceful",
                "style_suggestions": "Chill lo-fi beats with rain sounds, smooth hip hop flow",
                "target_audience": "Study music listeners, night owls",
                "emotional_tone": "Peaceful, introspective, melancholic",
                "visual_concepts": "Rainy city streets, neon signs, warm indoor lighting"
            }

        tracker.stop_timer("gemini_brief_generation")
        print(f"✅ Kūrybinė idėja sugeneruota: {brief['title']}")

        # Step 3: Create song directory
        print("\n📁 2/5 Kuriamas dainos aplankas...")
        song_dir = file_manager.create_song_directory(brief['title'])

        # Step 4: Generate music
        print("\n🎵 3/5 Generuojama muzika...")
        if use_real_apis and suno:
            generation_result = suno.generate_music_simple(prompt=brief['lyrics_prompt'])
            if not generation_result:
                raise Exception("Nepavyko pradėti muzikos generavimo")

            task_id = generation_result.get('taskId')
            print(f"✅ Užduotis pateikta Suno. Task ID: {task_id}")

            # Wait for completion
            print("\n⏳ 4/5 Laukiama užduoties užbaigimo...")
            task_result = suno.wait_for_generation_completion(task_id)
        else:
            # Mock generation
            generation_result = mock_suno_generation()
            task_id = generation_result['taskId']
            task_result = mock_wait_for_completion(task_id)

        # Step 5: Process files and create content
        print("\n⬇️ 5/6 Tvarkomi failai...")

        # Handle audio files
        tracks_data = task_result.get('data', [])
        audio_files = []

        if use_real_apis:
            # Download real audio files
            for i, track in enumerate(tracks_data, 1):
                audio_url = track.get('audio_url')
                if audio_url:
                    filename = f"track_{i}.mp3"
                    success = file_manager.download_file(audio_url, song_dir, filename)
                    if success:
                        audio_files.append(f"{song_dir}/{filename}")
                    else:
                        print(f"⚠️ Nepavyko atsisiųsti {filename}")
        else:
            # Copy mock audio files for testing
            mock_audio_dir = "mock_audio"
            if not os.path.exists(mock_audio_dir):
                os.makedirs(mock_audio_dir)
                print(f"⚠️ [MOCK] Sukurkite pavyzdinius MP3 failus aplanke: {mock_audio_dir}")
                print("   Pavyzdžiui: sample_track_1.mp3, sample_track_2.mp3")

            # Try to copy existing mock files
            for i in range(1, 3):  # Assume 2 tracks
                mock_file = f"{mock_audio_dir}/sample_track_{i}.mp3"
                target_file = f"{song_dir}/track_{i}.mp3"

                if os.path.exists(mock_file):
                    shutil.copy2(mock_file, target_file)
                    audio_files.append(target_file)
                    print(f"✅ [MOCK] Nukopijuotas {mock_file} → {target_file}")
                else:
                    print(f"⚠️ [MOCK] Mock failas nerastas: {mock_file}")

        # Step 6: Generate cover art and create videos
        print("\n🎨 6/6 Generuojamas viršelis ir video...")

        # Create cover art prompt
        cover_prompt = f"Album cover art for {brief['title']}, Lo-Fi Hip Hop music, rainy night in Tokyo, neon lights, atmospheric, professional design"

        # Generate cover image
        cover_filename = "cover.png"
        cover_path = f"{song_dir}/{cover_filename}"

        tracker.start_timer("image_generation")
        if (use_real_apis or use_hybrid) and image_client:
            print("🎨 Siunčiama užklausa į Stability AI... Tai gali užtrukti.")
            success = image_client.generate_image(cover_prompt, song_dir, cover_filename)
        else:
            print("⚠️ [MOCK] Realios paveikslėlių generacijos API nepasiekiama")
            print("   Įdėkite STABILITY_API_KEY į .env failą realiam testavimui")
            success = False

        tracker.stop_timer("image_generation")

        if success:
            print("✅ Viršelio paveikslėlis sugeneruotas")
            # Add file info to tracker
            cover_info = tracker.get_file_info(cover_path)
            if cover_info:
                tracker.add_metric("cover_image", cover_info)
        else:
            print("❌ Nepavyko sugeneruoti viršelio paveikslėlio")

        # Create videos from audio + image
        videos_created = 0
        if success and audio_files:
            for i, audio_file in enumerate(audio_files, 1):
                video_title = f"{brief['title']}_v{i}"
                video_filename = f"{video_title}.mp4"
                video_path = f"{song_dir}/{video_filename}"

                tracker.start_timer(f"video_creation_v{i}")
                video_success = video_creator.create_video_from_audio_and_image(
                    image_path=cover_path,
                    audio_path=audio_file,
                    output_path=song_dir,
                    title=video_title
                )
                tracker.stop_timer(f"video_creation_v{i}")

                if video_success:
                    videos_created += 1
                    print(f"✅ Video sukurtas: {video_filename}")

                    # Add video file info to tracker
                    video_info = tracker.get_file_info(video_path)
                    if video_info:
                        tracker.add_metric(f"video_{i}", video_info)
                else:
                    print(f"❌ Nepavyko sukurti video: {video_filename}")
        else:
            print("⚠️ Video kūrimas praleistas (nėra viršelio arba audio failų)")

        # Final summary
        print("\n" + "=" * 50)
        print("🎉 KŪRIMO CIKLAS UŽBAIGTAS!")
        print("=" * 50)
        print(f"📂 Failai išsaugoti: {song_dir}")
        print(f"🎵 Sukurta takelių: {len(audio_files)}")
        print(f"🖼️ Viršelio paveikslėlis: {'✅ Sukurtas' if success else '❌ Nepavyko'}")
        print(f"🎬 Video failai: {videos_created} sukurti")
        print("\n📋 Aplanko turinys:")
        contents = file_manager.list_directory_contents(song_dir)
        for item in contents:
            file_info = file_manager.get_file_info(f"{song_dir}/{item}")
            if file_info:
                size_mb = file_info['size'] / (1024 * 1024)
                print(f"  • {item} ({size_mb:.1f} MB)")
            else:
                print(f"  • {item}")

        # Generate and save technical report
        print("\n📊 Generuojama techninė ataskaita...")
        report = tracker.generate_report()
        print(report)

        # Save report to file
        tracker.save_report(song_dir)

        return {
            'success': True,
            'song_directory': song_dir,
            'tracks_count': len(audio_files),
            'videos_created': videos_created,
            'cover_generated': success,
            'brief': brief,
            'performance_report': report
        }

    except Exception as e:
        print(f"\n❌ KLAIDA: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def run_full_pipeline():
    """Run the complete autonomous pipeline: generate content + publish to YouTube"""
    print("🚀 PILNO CIKLO REŽIMAS: Generavimas + Publikavimas")
    print("=" * 60)
    print("⚠️  Šis režimas naudos realius API kreditus ir įkels video į YouTube!")
    print("🔒 Visi video bus įkelti kaip PRIVATE pagal nutylėjimą")
    print("=" * 60)

    # Initialize performance tracker
    tracker = PerformanceTracker()

    try:
        # Initialize all components
        load_dotenv()

        print("\n🔧 Inicijuojami komponentai...")

        # Initialize database manager
        db_manager = DatabaseManager()

        # Initialize clients
        suno = SunoClient()
        gemini = GeminiClient()
        image_client = ImageClient()
        youtube = YouTubeClient()
        file_manager = FileManager()
        video_creator = VideoCreator()

        print("✅ Visi komponentai inicijuoti sėkmingai")

        # Step 1: Generate creative brief with YouTube metadata
        print("\n🧠 1/6 Generuojama kūrybinė idėja su YouTube metaduomenimis...")
        tracker.start_timer("full_pipeline_brief")

        brief = gemini.generate_creative_brief(
            genre="Lo-Fi Hip Hop",
            theme="rainy night in Tokyo"
        )

        tracker.stop_timer("full_pipeline_brief")
        print(f"✅ Idėja sugeneruota: {brief['title']}")

        # Track content creation in database
        print("\n💾 Registruojama kūrybinė veikla duomenų bazėje...")
        creation_data = {
            'genre': "Lo-Fi Hip Hop",
            'theme': "rainy night in Tokyo",
            'title': brief['title'],
            'youtube_title': brief.get('youtube_title', brief['title']),
            'brief_json': json.dumps(brief),
            'status': 'brief_generated'
        }
        content_creation = db_manager.add_content_creation(creation_data)
        print(f"✅ Kūrybinė veikla užregistruota DB (ID: {content_creation.id})")

        # Step 2: Create song directory
        print("\n📁 2/6 Kuriamas projekto aplankas...")
        song_dir = file_manager.create_song_directory(brief['title'])

        # Step 3: Generate music
        print("\n🎵 3/6 Generuojama muzika...")
        tracker.start_timer("full_pipeline_music")

        generation_result = suno.generate_music_simple(prompt=brief['lyrics_prompt'])
        if not generation_result:
            raise Exception("Nepavyko pradėti muzikos generavimo")

        task_id = generation_result.get('taskId')
        print(f"✅ Užduotis pateikta Suno. Task ID: {task_id}")

        # Wait for completion
        print("\n⏳ 4/6 Laukiama muzikos užbaigimo...")
        task_result = suno.wait_for_generation_completion(task_id)

        tracker.stop_timer("full_pipeline_music")

        # Step 4: Process audio files
        print("\n⬇️ 5/6 Tvarkomi audio failai...")
        tracks_data = task_result.get('data', [])
        audio_files = []

        for i, track in enumerate(tracks_data, 1):
            audio_url = track.get('audio_url')
            if audio_url:
                filename = f"track_{i}.mp3"
                success = file_manager.download_file(audio_url, song_dir, filename)
                if success:
                    audio_files.append(f"{song_dir}/{filename}")
                    print(f"✅ Atsisiųstas {filename}")
                else:
                    print(f"⚠️ Nepavyko atsisiųsti {filename}")

        # Step 5: Generate cover and create videos
        print("\n🎨 6/6 Generuojamas viršelis ir video...")
        tracker.start_timer("full_pipeline_visuals")

        cover_prompt = f"Album cover art for {brief['title']}, Lo-Fi Hip Hop music, rainy night in Tokyo, neon lights, atmospheric, professional design"
        cover_filename = "cover.png"
        cover_path = f"{song_dir}/{cover_filename}"

        success = image_client.generate_image(cover_prompt, song_dir, cover_filename)

        if success:
            print("✅ Viršelio paveikslėlis sugeneruotas")

            # Create videos
            videos_created = []
            for i, audio_file in enumerate(audio_files, 1):
                video_title = f"{brief['title']} v{i}"
                video_filename = f"{video_title}.mp4"
                video_path = f"{song_dir}/{video_filename}"

                video_success = video_creator.create_video_from_audio_and_image(
                    image_path=cover_path,
                    audio_path=audio_file,
                    output_path=song_dir,
                    title=video_title
                )

                if video_success:
                    videos_created.append(video_path)
                    print(f"✅ Video sukurtas: {video_filename}")
                else:
                    print(f"❌ Nepavyko sukurti video: {video_filename}")

            tracker.stop_timer("full_pipeline_visuals")

            # Step 6: Upload videos to YouTube
            print("\n📤 7/7 Įkeliami video į YouTube...")
            uploaded_videos = []

            for i, video_path in enumerate(videos_created, 1):
                # Prepare YouTube metadata
                youtube_title = f"{brief['youtube_title']} v{i}" if 'youtube_title' in brief else f"{brief['title']} v{i}"
                youtube_description = brief.get('youtube_description', f"AI generated music: {brief['title']}\n\n{brief.get('description', '')}")
                youtube_tags = brief.get('youtube_tags', ['lofi', 'ai music', 'beats', 'study music'])

                print(f"\n🎬 Įkeliamas video {i}/{len(videos_created)}: {youtube_title}")

                tracker.start_timer(f"youtube_upload_v{i}")
                video_id = youtube.upload_video(
                    video_path=video_path,
                    title=youtube_title,
                    description=youtube_description,
                    tags=youtube_tags,
                    category_id='10',  # Music
                    privacy_status='private'  # Always private for safety
                )
                tracker.stop_timer(f"youtube_upload_v{i}")

                if video_id:
                    # Track YouTube video in database
                    video_data = {
                        'video_id': video_id,
                        'youtube_url': f"https://www.youtube.com/watch?v={video_id}",
                        'title': youtube_title,
                        'description': youtube_description,
                        'tags': youtube_tags,
                        'category_id': '10',
                        'privacy_status': 'private'
                    }
                    youtube_video = db_manager.add_youtube_video(content_creation, video_data)
                    print(f"✅ Video užregistruotas DB (ID: {youtube_video.id})")

                    uploaded_videos.append({
                        'video_id': video_id,
                        'title': youtube_title,
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })
                    print(f"✅ Video '{youtube_title}' sėkmingai įkeltas!")
                    print(f"🔗 Nuoroda: https://www.youtube.com/watch?v={video_id}")
                else:
                    print(f"❌ Nepavyko įkelti video: {youtube_title}")

            # Generate final report
            print("\n📊 Generuojama galutinė ataskaita...")
            report = tracker.generate_report()
            tracker.save_report(song_dir)

            return {
                'success': True,
                'song_directory': song_dir,
                'brief': brief,
                'tracks_count': len(audio_files),
                'videos_created': len(videos_created),
                'videos_uploaded': len(uploaded_videos),
                'uploaded_videos': uploaded_videos,
                'performance_report': report
            }

        else:
            print("❌ Nepavyko sugeneruoti viršelio paveikslėlio")
            return {
                'success': False,
                'error': 'Failed to generate cover image'
            }

    except Exception as e:
        print(f"\n❌ KLAIDA PILNAME CIKLE: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def run_analytics_collection():
    """Run YouTube analytics collection cycle"""
    print("📊 ANALYTICS COLLECTION CYCLE")
    print("=" * 40)

    try:
        # Initialize components
        load_dotenv()

        print("\n🔧 Inicijuojami komponentai...")

        # Initialize database manager
        db_manager = DatabaseManager()

        # Initialize YouTube client
        youtube_client = YouTubeClient()

        print("✅ Komponentai inicijuoti sėkmingai")

        # Create analytics collector
        collector = AnalyticsCollector(db_manager, youtube_client)

        # Run collection cycle
        result = collector.run_collection_cycle()

        return {
            'success': True,
            'message': result
        }

    except Exception as e:
        print(f"\n❌ Analytics collection failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def run_performance_analysis():
    """Run AI-powered performance analysis using Gemini"""
    print("🧠 AI-Powered Performance Analysis")
    print("=" * 40)

    try:
        # Initialize components
        load_dotenv()

        print("\n🔧 Inicijuojami komponentai...")

        # Initialize database manager
        db_manager = DatabaseManager()

        # Initialize Gemini client
        gemini_client = GeminiClient()

        print("✅ Komponentai inicijuoti sėkmingai")

        # Create performance analyzer
        analyzer = PerformanceAnalyzer(db_manager, gemini_client)

        # Run analysis
        analysis_result = analyzer.run_analysis()

        print("\n" + "=" * 80)
        print("📋 ANALYSIS RESULTS")
        print("=" * 80)
        print(analysis_result)

        return {
            'success': True,
            'analysis': analysis_result
        }

    except Exception as e:
        print(f"\n❌ Performance analysis failed: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def run_adaptive_cycle():
    """Run the complete adaptive learning cycle: Analysis + Adaptive Creation"""
    print("🚀 ADAPTYVUS CIKLAS - MOKYMASIS + KŪRYBA")
    print("=" * 60)
    print("🤖 Šis režimas sujungs analizę ir kūrybą į vieną protingą ciklą")
    print("📊 Sistema išmoks iš savo patirties ir pritaikys įžvalgas")
    print("=" * 60)

    try:
        # Initialize all components
        load_dotenv()

        print("\n🔧 Inicijuojami komponentai...")

        # Initialize database manager
        db_manager = DatabaseManager()

        # Initialize clients
        suno = SunoClient()
        gemini = GeminiClient()
        image_client = ImageClient()
        youtube = YouTubeClient()
        file_manager = FileManager()
        video_creator = VideoCreator()

        print("✅ Visi komponentai inicijuoti sėkmingai")

        # Step 1: Run Performance Analysis
        print("\n🧠 1/7 ANALIZĖS FAZĖ - Mokymasis iš duomenų...")
        print("-" * 50)

        analyzer = PerformanceAnalyzer(db_manager, gemini)
        analysis_result = analyzer.run_analysis()

        # Check if we have sufficient data for adaptive learning
        if analysis_result == "INSUFFICIENT_DATA":
            print("\n⚠️  Nepakanka duomenų adaptyviam mokymuisi")
            print("🔄 Pereinama į standartinį kūrybos režimą...")
            print("💡 Sistema kurs turinį remdamasi bendromis žiniomis")

            # Use standard creative brief generation (without analysis)
            analysis_report = None
        else:
            print("\n✅ Gautos analizės įžvalgos!")
            print("🎯 Sistema adaptuos kūrybą pagal šias rekomendacijas")
            analysis_report = analysis_result

        # Step 2: Generate Adaptive Creative Brief
        print("\n🧠 2/7 ADAPTYVI KŪRYBA - Generuojama idėja...")
        print("-" * 50)

        brief = gemini.generate_creative_brief(
            genre="Lo-Fi Hip Hop",
            theme="rainy night in Tokyo",
            analysis_report=analysis_report
        )

        print(f"✅ {('Adaptyvi' if analysis_report else 'Standartinė')} idėja sugeneruota: {brief['title']}")

        if analysis_report:
            print("🎯 Ši idėja buvo suformuota atsižvelgiant į:")
            print("   - Ankstesnių video sėkmės dėsningumus")
            print("   - Auditorijos pageidavimus")
            print("   - Optimizavimo rekomendacijas")

        # Step 3: Track content creation in database
        print("\n💾 3/7 Registruojama kūrybinė veikla duomenų bazėje...")
        creation_data = {
            'genre': "Lo-Fi Hip Hop",
            'theme': "rainy night in Tokyo",
            'title': brief['title'],
            'youtube_title': brief.get('youtube_title', brief['title']),
            'brief_json': json.dumps(brief),
            'status': 'adaptive_brief_generated'
        }
        content_creation = db_manager.add_content_creation(creation_data)
        print(f"✅ Kūrybinė veikla užregistruota DB (ID: {content_creation.id})")

        # Step 4: Create song directory
        print("\n📁 4/7 Kuriamas projekto aplankas...")
        song_dir = file_manager.create_song_directory(brief['title'])

        # Step 5: Generate music
        print("\n🎵 5/7 Generuojama muzika...")
        generation_result = suno.generate_music_simple(prompt=brief['lyrics_prompt'])
        if not generation_result:
            raise Exception("Nepavyko pradėti muzikos generavimo")

        task_id = generation_result.get('taskId')
        print(f"✅ Užduotis pateikta Suno. Task ID: {task_id}")

        # Wait for completion
        print("\n⏳ 6/7 Laukiama muzikos užbaigimo...")
        task_result = suno.wait_for_generation_completion(task_id)

        # Step 6: Process audio files
        print("\n⬇️ 7/7 Tvarkomi audio failai...")
        tracks_data = task_result.get('data', [])
        audio_files = []

        for i, track in enumerate(tracks_data, 1):
            audio_url = track.get('audio_url')
            if audio_url:
                filename = f"track_{i}.mp3"
                success = file_manager.download_file(audio_url, song_dir, filename)
                if success:
                    audio_files.append(f"{song_dir}/{filename}")
                    print(f"✅ Atsisiųstas {filename}")
                else:
                    print(f"⚠️ Nepavyko atsisiųsti {filename}")

        # Step 7: Generate cover and create videos
        print("\n🎨 8/8 Generuojamas viršelis ir video...")
        cover_prompt = f"Album cover art for {brief['title']}, Lo-Fi Hip Hop music, rainy night in Tokyo, neon lights, atmospheric, professional design"
        cover_filename = "cover.png"
        cover_path = f"{song_dir}/{cover_filename}"

        success = image_client.generate_image(cover_prompt, song_dir, cover_filename)

        if success:
            print("✅ Viršelio paveikslėlis sugeneruotas")

            # Create videos
            videos_created = []
            for i, audio_file in enumerate(audio_files, 1):
                video_title = f"{brief['title']} v{i}"
                video_filename = f"{video_title}.mp4"
                video_path = f"{song_dir}/{video_filename}"

                video_success = video_creator.create_video_from_audio_and_image(
                    image_path=cover_path,
                    audio_path=audio_file,
                    output_path=song_dir,
                    title=video_title
                )

                if video_success:
                    videos_created.append(video_path)
                    print(f"✅ Video sukurtas: {video_filename}")
                else:
                    print(f"❌ Nepavyko sukurti video: {video_filename}")

            # Step 8: Upload videos to YouTube
            print("\n📤 9/9 Įkeliami video į YouTube...")
            uploaded_videos = []

            for i, video_path in enumerate(videos_created, 1):
                # Prepare YouTube metadata
                youtube_title = f"{brief['youtube_title']} v{i}" if 'youtube_title' in brief else f"{brief['title']} v{i}"
                youtube_description = brief.get('youtube_description', f"AI generated music: {brief['title']}\n\n{brief.get('description', '')}")
                youtube_tags = brief.get('youtube_tags', ['lofi', 'ai music', 'beats', 'study music'])

                print(f"\n🎬 Įkeliamas video {i}/{len(videos_created)}: {youtube_title}")

                video_id = youtube.upload_video(
                    video_path=video_path,
                    title=youtube_title,
                    description=youtube_description,
                    tags=youtube_tags,
                    category_id='10',  # Music
                    privacy_status='private'  # Always private for safety
                )

                if video_id:
                    # Track YouTube video in database
                    video_data = {
                        'video_id': video_id,
                        'youtube_url': f"https://www.youtube.com/watch?v={video_id}",
                        'title': youtube_title,
                        'description': youtube_description,
                        'tags': youtube_tags,
                        'category_id': '10',
                        'privacy_status': 'private'
                    }
                    youtube_video = db_manager.add_youtube_video(content_creation, video_data)
                    print(f"✅ Video užregistruotas DB (ID: {youtube_video.id})")

                    uploaded_videos.append({
                        'video_id': video_id,
                        'title': youtube_title,
                        'url': f"https://www.youtube.com/watch?v={video_id}"
                    })
                    print(f"✅ Video '{youtube_title}' sėkmingai įkeltas!")
                    print(f"🔗 Nuoroda: https://www.youtube.com/watch?v={video_id}")
                else:
                    print(f"❌ Nepavyko įkelti video: {youtube_title}")

            # Final summary
            print("\n" + "=" * 80)
            print("🎉 ADAPTYVUS CIKLAS UŽBAIGTAS - SISTEMA IŠMOKE!")
            print("=" * 80)
            print(f"📂 Failai išsaugoti: {song_dir}")
            print(f"🎵 Sukurta takelių: {len(audio_files)}")
            print(f"🖼️ Viršelio paveikslėlis: ✅ Sukurtas")
            print(f"🎬 Video failai: {len(videos_created)} sukurti")
            print(f"📤 Įkelta į YouTube: {len(uploaded_videos)} video")

            if analysis_report:
                print(f"\n🎯 ADAPTYVUMO LAIPSNIS:")
                print(f"   ✅ Sistema pritaikė {len(analysis_result.split())} simbolių analizės duomenis")
                print(f"   ✅ Kūryba buvo optimizuota pagal istorinius duomenis")
                print(f"   🤖 Sistema evoliucionuoja ir mokosi!")

            return {
                'success': True,
                'song_directory': song_dir,
                'brief': brief,
                'tracks_count': len(audio_files),
                'videos_created': len(videos_created),
                'videos_uploaded': len(uploaded_videos),
                'uploaded_videos': uploaded_videos,
                'adaptive_mode': analysis_report is not None,
                'analysis_used': analysis_report is not None
            }

        else:
            print("❌ Nepavyko sugeneruoti viršelio paveikslėlio")
            return {
                'success': False,
                'error': 'Failed to generate cover image'
            }

    except Exception as e:
        print(f"\n❌ KLAIDA ADAPTYVIAME CIKLE: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Main function with user choice"""
    print("🎵 AUTONOMINIS MUZIKANTAS")
    print("=" * 30)

    # Ask user for mode
    while True:
        print("\nPasirinkite veikimo režimą:")
        print("1. 🧪 Testavimo režimas (Mock duomenys)")
        print("2. 🔑 Realus režimas (Reikalingi API raktai)")
        print("3. 🔄 Hibridinis testas (Realus vaizdas / Mock garsas)")
        print("4. 🎥 Testuoti YouTube prisijungimą")
        print("5. 🚀 Vykdyti Pilną Ciklą (Generuoti ir Publikuoti)")
        print("6. 📊 Atnaujinti Video Statistiką")
        print("7. 🧠 Atlikti Našumo Analizę")
        print("8. � Vykdyti Adaptyvų Ciklą (Mokymasis + Kūryba)")
        print("9. �🚪 Išeiti")

        choice = input("\nJūsų pasirinkimas (1-8): ").strip()

        if choice == "1":
            print("\n🧪 Paleidžiamas TESTAVIMO REŽIMAS...")
            result = run_creation_pipeline(use_real_apis=False, use_hybrid=False)
            break
        elif choice == "2":
            print("\n🔑 Paleidžiamas REALUS REŽIMAS...")
            print("⚠️  Įsitikinkite, kad .env faile yra teisingi API raktai!")
            confirm = input("Ar tikrai norite tęsti? (y/N): ").strip().lower()
            if confirm == 'y':
                result = run_creation_pipeline(use_real_apis=True, use_hybrid=False)
                break
            else:
                continue
        elif choice == "3":
            print("\n🔄 Paleidžiamas HIBRIDINIS TESTAS...")
            print("📝 Šis režimas naudos realią paveikslėlių generaciją, bet mock audio")
            print("⚠️  Įsitikinkite, kad .env faile yra STABILITY_API_KEY!")
            confirm = input("Ar tikrai norite tęsti? (y/N): ").strip().lower()
            if confirm == 'y':
                result = run_creation_pipeline(use_real_apis=False, use_hybrid=True)
                break
            else:
                continue
        elif choice == "4":
            print("\n🎥 TESTUOJAMAS YOUTUBE PRISIJUNGIMAS...")
            print("⚠️  Įsitikinkite, kad .env faile yra YOUTUBE_CHANNEL_ID!")
            print("⚠️  Įsitikinkite, kad configs/client_secrets.json egzistuoja!")
            confirm = input("Ar tikrai norite tęsti? (y/N): ").strip().lower()
            if confirm == 'y':
                result = test_youtube_connection()
                break
            else:
                continue
        elif choice == "5":
            print("\n🚀 PILNO CIKLO REŽIMAS...")
            print("⚠️  Šis režimas naudos realius API kreditus!")
            print("⚠️  Įsitikinkite, kad turite:")
            print("   - SUNO_API_KEY")
            print("   - GEMINI_API_KEY")
            print("   - STABILITY_API_KEY")
            print("   - YOUTUBE_CHANNEL_ID")
            print("   - configs/client_secrets.json")
            confirm = input("\nAr tikrai norite pradėti pilną ciklą? (y/N): ").strip().lower()
            if confirm == 'y':
                result = run_full_pipeline()
                break
            else:
                continue
        elif choice == "6":
            print("\n📊 ATNAUJINAMOS VIDEO STATISTIKOS...")
            print("⚠️  Įsitikinkite, kad turite įkeltų video duomenų bazėje!")
            print("⚠️  Įsitikinkite, kad configs/client_secrets.json egzistuoja!")
            confirm = input("Ar tikrai norite atnaujinti statistiką? (y/N): ").strip().lower()
            if confirm == 'y':
                result = run_analytics_collection()
                break
            else:
                continue
        elif choice == "7":
            print("\n🧠 ATLIKINAMA NAŠUMO ANALIZĖ...")
            result = run_performance_analysis()
            break
        elif choice == "8":
            print("\n🚀 PALEIDŽIAMAS ADAPTYVUS CIKLAS...")
            print("⚠️  Šis režimas naudos realius API kreditus!")
            print("⚠️  Įsitikinkite, kad turite:")
            print("   - SUNO_API_KEY")
            print("   - GEMINI_API_KEY")
            print("   - STABILITY_API_KEY")
            print("   - YOUTUBE_CHANNEL_ID")
            print("   - configs/client_secrets.json")
            confirm = input("\nAr tikrai norite pradėti adaptyvų ciklą? (y/N): ").strip().lower()
            if confirm == 'y':
                result = run_adaptive_cycle()
                break
            else:
                continue
        elif choice == "9":
            print("\n👋 Viso gero!")
            return
        else:
            print("❌ Neteisingas pasirinkimas. Bandykite dar kartą.")

    # Show results
    if result['success']:
        print("\n✅ Procesas sėkmingai užbaigtas!")
        if 'song_directory' in result:
            print(f"📂 Rezultatai: {result['song_directory']}")
        if 'videos_uploaded' in result:
            print(f"🎬 Įkelta video į YouTube: {result['videos_uploaded']}")
            if result['uploaded_videos']:
                print("\n📋 Įkelti video:")
                for video in result['uploaded_videos']:
                    print(f"  • {video['title']}")
                    print(f"    🔗 {video['url']}")
    else:
        print(f"\n❌ Įvyko klaida: {result['error']}")

if __name__ == "__main__":
    main()
