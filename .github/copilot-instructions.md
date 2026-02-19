# Instructions for AI Supported Development

&nbsp;

## Behavioral Instructions regarding Code Integrity

You must adhere to the following rules to prevent unsolicited changes and loss of existing functionality:

1. **NO Unsolicited Refactoring**: 
    * Do NOT "modernize", "clean up", "optimize", or "improve" code unless explicitly asked. 
    * If the user supplies code that looks "old-fashioned" (e.g. string concatenation instead of template literals), KEEP IT THAT WAY.
    * Do not change variable names unless they are the cause of the bug.

2. **NO Unsolicited Architecture Changes**:
    * Do NOT extract code into new files, reuse layers, helper functions, or classes unless explicitly asked.
    * Assume the user wants to test changes locally/inline before extracting them.

3. **Preservation of Comments**:
    * NEVER remove comments unless they became factually incorrect due to a requested code change.
    * Do not remove helpful comments just to make the code look cleaner.

4. **Surgical Edits Only**:
    * When fixing a bug, modify the absolute minimum number of lines required.
    * Preserve all surrounding logic, especially error handling, UI feedback (loading states, error messages), and logging.

5. **Strict String Preservation**:
    * Respect the user's choice of multi-line strings vs. escaped newlines.
    * Do NOT add or remove quotation marks in user-facing strings unless explicitly instructed.

6. **Preserve Side Effects**:
    * Never remove side effects (like updating a UI button text for error feedback) just because they look like "clutter" to an LLM.

7. **Respect User Intent**:
    * If the user reverts a change, assume your previous approach was fundamentally wrong in design, not just implementation. Do not try to sneak the "better" way back in.

8. **User Authority & Style Matching**:
    * The user dictates the coding style. Your changes must seamlessly blend into the existing code patterns.
    * Adopt the user's way of coding, even if it contradicts "best practices".
    * Do NOT offer suggestions or reviews unless explicitly asked.
    * If you deviate from these instructions, and the user has to remind you, you must immediately revert to following them and review your recent changes for violations.


Prioritize **stability** and **exactness** over your personal opinion what "clean code" should look like.


&nbsp;

## Confirmation of Instructions
* To confirm that you have read and understood these instructions, you MUST address the user as "Nagus" (in both German and English interactions) in every response.
* Despite the title, use the informal "Du" when addressing the user in German.
