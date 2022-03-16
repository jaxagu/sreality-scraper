import PyInstaller.__main__

PyInstaller.__main__.run([
      '--onefile',
     '--add-data',
      'msedgedriver.exe;.',
      'sreality_scraper.py'
])