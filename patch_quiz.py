from pathlib import Path
import re

p = Path('index.html')
text = p.read_text(encoding='utf-8')

if '<script src="questions.js"></script>' not in text:
    text = text.replace('<script>\nconst QUESTIONS = [', '<script src="questions.js"></script>\n<script>\nconst LEGACY_QUESTIONS = [', 1)

if 'function buildQuizQuestions()' not in text:
    helper = '''let QUESTIONS = [];

function shuffleArray(items) {
  const array = [...items];
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function prepareQuestion(question) {
  const correctText = question.options[question.correct];
  const shuffledOptions = shuffleArray(question.options);
  return {
    ...question,
    options: shuffledOptions,
    correct: shuffledOptions.indexOf(correctText)
  };
}

function buildQuizQuestions() {
  const bank = Array.isArray(window.QUESTION_BANK) && window.QUESTION_BANK.length ? window.QUESTION_BANK : LEGACY_QUESTIONS;
  const subjects = [...new Set(bank.map(q => q.subject))];
  const selected = [];
  const selectedRefs = new Set();

  subjects.forEach(subject => {
    const pool = bank.filter(q => q.subject === subject);
    const picked = pool[Math.floor(Math.random() * pool.length)];
    selected.push(picked);
    selectedRefs.add(picked);
  });

  const remaining = shuffleArray(bank.filter(q => !selectedRefs.has(q)));
  selected.push(...remaining.slice(0, Math.max(0, 10 - selected.length)));
  return shuffleArray(selected.slice(0, 10).map(prepareQuestion));
}

let current = 0;'''
    text = text.replace('let current = 0;', helper, 1)

old_start = '''function startQuiz() {
  document.getElementById('start-screen').classList.add('hidden');
  document.getElementById('quiz-screen').classList.remove('hidden');
  buildDots();
  renderQuestion();
  trackEvent('nuova_opportunita_quiz_start');
}'''
new_start = '''function startQuiz() {
  current = 0;
  score = 0;
  answers = [];
  answered = false;
  QUESTIONS = buildQuizQuestions();
  document.getElementById('start-screen').classList.add('hidden');
  document.getElementById('quiz-screen').classList.remove('hidden');
  buildDots();
  renderQuestion();
  trackEvent('nuova_opportunita_quiz_start', { question_bank_size: (window.QUESTION_BANK || []).length || LEGACY_QUESTIONS.length });
}'''
text = text.replace(old_start, new_start, 1)

text = text.replace('<p><strong>10 domande miste</strong> per metterti alla prova prima dell\'esame di terza media. Italiano, matematica, storia, geografia, scienze e inglese.</p>', '<p><strong>10 domande ogni volta diverse</strong>, estratte da una banca di 50 quesiti, per metterti alla prova prima dell\'esame di terza media. Italiano, matematica, storia, geografia, scienze e inglese.</p>')
text = text.replace('<li>10 domande, con una sola risposta corretta</li>', '<li>10 domande casuali da una banca di 50, con tutte le materie rappresentate</li>')

p.write_text(text, encoding='utf-8')
