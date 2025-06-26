# books/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book
from .utils import (
    process_wikipedia_info,
    generate_author_gpt_info,
    generate_audio_script,
    create_tts_audio
)
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Book)
def enrich_book_data(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        wiki_summary = process_wikipedia_info(instance)
        if not wiki_summary:
            wiki_summary = "위키피디아 정보 없음"

        author_info, author_works = generate_author_gpt_info(instance, wiki_summary)

        instance.author_info = author_info or "작가 정보를 가져오지 못했습니다."
        instance.author_works = author_works or ""

        try:
            script = generate_audio_script(instance, wiki_summary)
            audio_path = create_tts_audio(instance, script)
            instance.tts_audio = audio_path
        except Exception as audio_err:
            logger.warning(f"TTS 생성 중 오류 발생: {audio_err}")
            instance.tts_audio = None

        instance.save()

    except Exception as e:
        logger.error(f"도서 enrichment 실패 (Book ID: {instance.pk}): {e}")
