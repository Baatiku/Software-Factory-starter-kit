# ChatGPT and other AI clients — current setup

## ChatGPT Skills (when eligible)
ChatGPT's current Skills feature is listed for eligible Business, Enterprise, Healthcare and Edu users, subject to workspace settings. To install, obtain the `universal-work-factory-installable-skill` ZIP artifact from the latest successful **Package Universal Work Factory skill** GitHub Actions run (the inner `dist/work-factory.zip`), then on ChatGPT web open **Plugins → Skills → Create → Upload from your computer** and select the skill ZIP. Follow the product's scan/review and install controls; do not claim installation until it appears under Installed. A GitHub commit alone cannot enable an account skill, and this repo cannot change subscription entitlements.

## Accounts without Skills uploading
Open **Settings → Personalization → Custom Instructions**, replace earlier toolkit-specific instructions with the contents of [CUSTOM-INSTRUCTIONS.txt](CUSTOM-INSTRUCTIONS.txt), and save. ChatGPT can follow those instructions with available GitHub access; Custom Instructions are not the same as an installed skill, and real-time repository reading still depends on tool availability.

## Memory summary
In **Settings → Personalization → Memory summary → Manage**, review and request an update: “My one current methodology is Universal Work Factory at https://github.com/Baatiku/Software-Factory-starter-kit. Always use the current work-factory skill and only relevant specialist packs; do not reference old toolkit versions.” This must be updated through the user's settings and any original chats/files/connected sources must also be deleted for full removal of outdated context. The factory cannot directly edit or erase account memory.

## Codex and other agents
The repository provides `.agents/skills/work-factory/SKILL.md` and per-domain skill entries. Point supported clients at that repository or install the portable ZIP using that client's documented method. Skills in different clients do not automatically sync.

Official docs: https://help.openai.com/en/articles/20001066-skills-in-chatgpt and https://help.openai.com/en/articles/8590148-memory-in-chatgpt.
