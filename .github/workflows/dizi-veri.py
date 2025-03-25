name: Fetch TV Shows and Save to File

on:
  schedule:
    - cron: '15 0 * * *'  # Her gün gece 00:15'te çalışacak
  workflow_dispatch:

jobs:
  fetch-tv-shows:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install beautifulsoup4 requests  # Gerekli Python kütüphanelerini yükle

    - name: Run TV Shows Fetching Script
      run: |
        python dizi_günlük.py  # Python dosyanızın adı buraya yazılacak

    - name: Commit and push updated TV shows list
      run: |
        git config --global user.name "GitHub Actions"
        git config --global user.email "actions@github.com"

        # Değişiklikleri kontrol et
        git pull origin main  # Güncellemeleri çek
        if git diff --quiet; then
          echo "No changes detected. Skipping commit."
        else
          git add diziler.txt
          git commit -m "Otomatik olarak güncellenmiş dizi listesi"
          git push
        fi
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
