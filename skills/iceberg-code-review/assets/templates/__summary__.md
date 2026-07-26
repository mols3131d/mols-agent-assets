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

## Details

| 🔴 `p0` | 🟠 `p1` | 🟡 `p2` | 🟢 `p3` | 🔵 `p4` |
| :---: | :---: | :---: | :---: | :---: |
| {{p0_count}} | {{p1_count}} | {{p2_count}} | {{p3_count}} | {{p4_count}} |

---

### {{priority_emoji}} [`{{domain}}-{{detail}}`]({{link}}) <!-- Link only if detail doc exists -->

[`{{file}}:{{start_line}}[-{{end_line}}]`]({{link}})

- **{{focus}} {{core}}**: {{observation}}

  ---> **{{action}} {{what}}**: {{recommendation}}

---

### {{additional_detail_heading}}    <!-- Write Another Detail -->

[`{{file}}:{{start_line}}[-{{end_line}}]`]({{link}})

- **{{focus}} {{core}}**: {{observation}}

  ---> **{{action}} {{what}}**: {{recommendation}}

---
