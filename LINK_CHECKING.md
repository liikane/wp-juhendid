# Dokumentatsiooni linkide kontroll

Kontroll käib lokaalselt ega tee võrgupäringuid. Käivita hoidla juurkaustast:

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_links.py
```

Kontrollija leiab Markdowni ja HTMLi suhtelised `href`-, `src`- ja Markdowni lingid, kontrollib failide ning HTML-i ID-de ja Markdowni pealkirjade olemasolu ning käsitleb URL-i fragmendi protsendikodeeringut. Koodiplokkide, Markdowni koodinäidete ja HTML-i `<pre>`/`<code>` sisu jäetakse vahele. Välislinke ei avata ega kontrollita.

## Välislingid, mida ei kontrollitud

Need juhendites kasutatud aktiivsed välislingid jäid võrguühenduseta kontrollimata:

- https://github.com
- https://git-scm.com/
- https://docs.github.com/en/get-started/quickstart
- https://www.git-scm.com/book/et/v2
- https://github.com/WordPress/agent-skills
- https://github.com/WordPress/agent-skills/blob/trunk/README.md
- https://github.com/WordPress/agent-skills/blob/trunk/docs/principles.md
- https://github.com/WordPress/agent-skills/blob/trunk/docs/authoring-guide.md
- https://github.com/WordPress/agent-skills/blob/trunk/docs/compatibility-policy.md
- https://github.com/WordPress/agent-skills/blob/trunk/docs/skill-set-v1.md
- https://github.com/WordPress/agent-skills/blob/trunk/docs/packaging.md
- https://github.com/WordPress/agent-skills/blob/trunk/docs/ai-authorship.md
- https://github.com/WordPress/agent-skills/blob/trunk/skills/wordpress-router/references/decision-tree.md
- https://github.com/WordPress/agent-skills/blob/trunk/skills/wp-project-triage/references/triage.schema.json
- https://github.com/WordPress/agent-skills/blob/trunk/skills/wp-plugin-development/references/security.md
- https://github.com/WordPress/agent-skills/tree/trunk/eval/scenarios
- https://raw.githubusercontent.com/liikane/wp-juhendid/main/img/wordpress-agent-skills-01.png
- https://raw.githubusercontent.com/liikane/wp-juhendid/main/img/wordpress-agent-skills-02.png
- https://raw.githubusercontent.com/liikane/wp-juhendid/main/img/wordpress-agent-skills-03.png
- https://raw.githubusercontent.com/liikane/wp-juhendid/main/img/wordpress-agent-skills-04.png

Näidislingid ja näidispildid Markdowni Cheat Sheetides on koodinäidete sees, mitte aktiivsed lingid.
