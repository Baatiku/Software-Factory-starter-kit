# Activate Software Factory in ChatGPT and Codex

This kit cannot change account settings or install an account-wide skill for you.

## Universal ChatGPT trigger
1. Settings → Personalization → Custom Instructions. Enable customization.
2. Paste install/CUSTOM-INSTRUCTIONS.txt, review and save. Custom Instructions apply across chats.
3. Optionally go to Settings → Personalization → Memory summary → Manage and request that install/MEMORY-SUMMARY-PROPOSAL.txt is reflected in your memory summary. This is not a direct memory edit.

## ChatGPT Skills (eligible accounts only)
Per OpenAI's October 2026 documentation, general ChatGPT skill creation and upload is available to eligible Business, Enterprise, Healthcare and Edu accounts, subject to workspace settings. For eligible accounts: Plugins → Skills → Create → Upload from your computer, then select the ZIP built by running python scripts/package_skill.py. Review and install in the UI. Plus cannot assume this capability; use Custom Instructions for universal triggering.

## Codex skill
Run python scripts/package_skill.py. Extract the archive so that the skill file exists at ~/.agents/skills/software-factory/SKILL.md (Windows: %USERPROFILE%\.agents\skills\software-factory\SKILL.md), with sibling references/, templates/ and scripts/ folders. Reload/restart Codex and verify skill discovery. A Codex installation is not a ChatGPT installation.

## Verification
Start a new chat and say: "I have a new software product idea." Confirm that the full factory methodology is considered without pasting the master prompt. The latest GitHub repository remains source of truth; if it cannot be fetched, the assistant must disclose that rather than invent updates.

Official docs:
https://help.openai.com/en/articles/20001066-skills-in-chatgpt/
https://help.openai.com/en/articles/8096356-custom-instructions-for-chatgpt
