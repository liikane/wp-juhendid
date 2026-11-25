# Kuidas kasutada Github Workflow

Skeem, kuhu paigutada .sh failid 

/homepage
│
├── generate_readme.sh      <--- SIIN asub skript
├── README_HEADER.md        <--- Staatiline esiosa (mida tahad alles hoida)
├── README.md               <--- Genereeritakse skriptiga
├── GITHUB_ALUSTAJA_JUHEND.md
├── Markdown_Cheat_sheet_ENG.html
├── Markdown_cheat_sheet_EST.html
├── ... teised failid ...
└── .github/
    └── workflows/
        └── update-readme.yml
