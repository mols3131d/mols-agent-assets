---
title: '{{Title}}'
date: 'yyyy-MM-dd'
type: 'code-review-summary'
---

<!--
Code review summary report template.
-->
## Summary

<!-- Summarize test results below -->

| 🟩 `PASS` | 🟥 `FAIL` | 🟧 `ERROR` | ⬜ `SKIP` |
| :---: | :---: | :---: | :---: |
| {{pass_count}} | {{fail_count}} | {{error_count}} | {{skip_count}} |

<!-- Write Summary -->

## Findings Details

| 🔴 `p0` | 🟠 `p1` | 🟡 `p2` | 🟢 `p3` | 🔵 `p4` |
| :---: | :---: | :---: | :---: | :---: |
| {{p0_count}} | {{p1_count}} | {{p2_count}} | {{p3_count}} | {{p4_count}} |

---

### {{priority_emoji}} [`{{domain}}-{{finding}}`]({{link}}) <!-- Link only if finding doc exists -->

[`{{file}}:{{start_line}}[-{{end_line}}]`]({{link}})

- **{{focus}} {{core}}**: {{observation}}

  ---> **{{action}} {{what}}**: {{recommendation}}

---

### {{additional_finding_heading}}    <!-- Write Another Finding -->

[`{{file}}:{{start_line}}[-{{end_line}}]`]({{link}})

- **{{focus}} {{core}}**: {{observation}}

  ---> **{{action}} {{what}}**: {{recommendation}}

---
