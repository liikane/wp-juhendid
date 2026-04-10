# Kuidas kasutada Github Workflow

Skeem, kuhu paigutada .sh failid 

/homepage
│
├── generate_readme.sh      <--- SIIN asub skript
├── README_HEADER.md        <--- Staatiline esiosa (mida tahad alles hoida)
├── README.md               <--- Genereeritakse skriptiga
├── GITHUB_ALUSTAJA_JUHEND.md
├── MarkDown_Cheat_sheet_ENG.html
├── MarkDown_cheat_sheet_EST.html
├── ... teised failid ...
└── .github/
    └── workflows/
        └── update-readme.yml
