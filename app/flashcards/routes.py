import json
import os
from pathlib import Path

from flask import Blueprint, render_template, abort

flashcards = Blueprint('flashcards', __name__, template_folder='templates/flashcards')


@flashcards.route('/')
def index():
    return render_template('flashcards-menu.html')

@flashcards.route('/indoeu')
def flashcards_indoeu():
    with open('app/flashcards/data/indoeu.json', encoding='utf-8') as f:
        languages = json.load(f)
    return render_template('flashcards-indoeu.html', languages=languages)