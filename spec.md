# AI SPEC — [PI-RAG Checker] · Nhóm [Agent-Red-E403] · Zone [E403]
Hướng: [] A — VLearn  [ ] B — Trợ lý Học viên  [x] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

## §1. User & Job

### Job executor + workflow

**Job executor chính:** Security Assessor / thành viên phụ trách AI Security.

**Người phối hợp:**

* AI Project Owner.
* AI/ML Engineer.
* RAG/Data Engineer.
* QA/DevSecOps.
* PM và BA.

**Workflow chính:**

* Workflow dự án khi không sử dụng AI
1. Security Assessor đọc policy, system behavior và bề mặt tấn công của hệ thống mục tiêu.
2. Người kiểm thử tự nghĩ và viết từng prompt tấn công.
3. Prompt được gửi thủ công đến hệ thống mục tiêu.
4. Người kiểm thử đọc phản hồi, tự đánh giá lý do thất bại hoặc thành công.
5. Nếu chưa đạt mục tiêu, người kiểm thử tự sửa cách diễn đạt, đổi chiến thuật và thử lại.
6. Kết quả được ghi vào bảng test, finding và báo cáo bằng tay.
7. Khi hệ thống thay đổi model, prompt hoặc corpus, nhóm phải lặp lại phần lớn quy trình.

* Đánh giá hạn chế: Khả năng tìm lỗ hổng phụ thuộc vào kinh nghiệm cá nhân; số biến thể prompt ít; quá trình thử–sai, ghi log và tổng hợp finding tốn thời gian; khó khám phá chiến thuật mới ngoài những gì người kiểm thử đã biết.

* Workflow dự án khi có sử dụng AI
1. Security Assessor cung cấp mục tiêu tấn công, phạm vi, policy, canary, RAG sandbox, giới hạn lượt và ngân sách; không cung cấp sẵn toàn bộ chuỗi prompt.
2. AI phân tích mục tiêu và sinh prompt tấn công đầu tiên từ seed, taxonomy và thông tin hệ thống được phép sử dụng.
3. Prompt được gửi tới target trong sandbox; toàn bộ response, retrieval trace, tool call và evaluator score được lưu.
4. AI phân tích phản hồi để nhận biết chiến thuật nào bị chặn, phần nào có tín hiệu tiến triển và điểm yếu nào có thể tiếp tục khai thác.
5. AI cập nhật attack memory gồm chiến thuật, prompt, kết quả, score, target state và feedback của reviewer.
6. Dựa trên memory, AI tự chọn bước tiếp theo: khai thác chiến thuật đang hiệu quả, thử chiến thuật mới hoặc kết hợp nhiều chiến thuật.
7. AI tự sinh prompt mới cho lượt tiếp theo; prompt phải khác về chiến lược hoặc cấu trúc, không chỉ thay từ đồng nghĩa.
8. Vòng lặp tiếp tục đến khi đạt objective, hết ngân sách, đạt giới hạn lượt, không còn cải thiện hoặc người vận hành kích hoạt kill switch.
9. Rule-based evaluator kiểm tra bằng chứng xác định; AI evaluator đề xuất label, confidence, severity và nguyên nhân.
10. Security Assessor xác nhận finding quan trọng, sửa nhãn sai và đưa feedback đã duyệt trở lại memory.
11. Hệ thống tạo regression objective và báo cáo so sánh khả năng tấn công trước–sau khi target được khắc phục.

* “Tự học” trong dự án này là adaptive learning từ response, score và feedback trong quá trình kiểm thử; prototype không tự fine-tune, không thay đổi trọng số mô hình và không tự mở rộng phạm vi kiểm thử.

### Core JTBD

> Khi cần đánh giá một hệ thống ngôn ngữ trước khi phát hành, tôi cần một quy trình có thể tự khám phá và điều chỉnh cách tấn công dựa trên phản hồi của target, để tìm được các lỗ hổng mà bộ prompt cố định hoặc kiểm thử thủ công có thể bỏ sót.

### Problem statement

Các đội phát triển hệ thống ngôn ngữ đang phụ thuộc vào prompt tấn công viết sẵn hoặc kinh nghiệm cá nhân, khiến phạm vi kiểm thử hẹp, khó thích ứng với phản hồi của từng target và tốn nhiều công sức khi phải liên tục tạo, chỉnh sửa, chạy lại và đánh giá prompt.

### Evidence

#### Số liệu mining / kết quả khảo sát

**Trạng thái:** 

Khảo sát thu được 23 phản hồi; riêng câu hỏi về mức độ khó có 22 phản hồi và câu hỏi mở có 5 phản hồi. Thành phần người tham gia gồm 13/23 AI Engineer (56,5%), 8/23 Software Engineer (34,8%), 1/23 giảng viên/mentor (4,3%) và 1/23 sinh viên (4,3%). Có 21/23 người (91,3%) đã từng sử dụng hoặc đang phát triển AI Agent, cho thấy phần lớn người trả lời có trải nghiệm liên quan trực tiếp đến bài toán.

Về công nghệ, 17/23 người (73,9%) từng sử dụng RAG, 16/23 (69,6%) dùng ChatGPT API, 12/23 (52,2%) dùng LangGraph, 11/23 (47,8%) dùng OpenAI Agents SDK và 6/23 (26,1%) dùng MCP. Tỷ lệ sử dụng RAG cao cho thấy nhu cầu kiểm thử RAG Poisoning có liên quan trực tiếp đến nhóm người dùng mục tiêu.

Về phương pháp kiểm thử, 14/23 người (60,9%) vẫn kiểm thử bằng prompt thủ công hoặc tự viết test script, trong khi chỉ 4/23 người (17,4%) sử dụng công cụ đánh giá chuyên dụng; 4/23 (17,4%) phải nhờ người khác kiểm thử và 1/23 (4,3%) dùng phương pháp khác. Kết quả này cho thấy quy trình hiện tại còn phân tán, phụ thuộc vào thao tác thủ công và chưa có một công cụ kiểm thử thống nhất.

Các vấn đề từng gặp khi phát triển AI Agent gồm: 9/23 người (39,1%) gặp hallucination, 5/23 (21,7%) gặp tình trạng agent tiết lộ thông tin không nên tiết lộ, 4/23 (17,4%) gặp hành động ngoài mong muốn, 2/23 (8,7%) gặp Prompt Injection, 2/23 (8,7%) gặp trường hợp agent gọi sai tool và 1/23 (4,3%) không biết cách kiểm thử đầy đủ. Nếu gộp bốn vấn đề bảo mật trực tiếp gồm Prompt Injection, rò rỉ thông tin, gọi sai tool và hành động ngoài mong muốn, có 13/23 người (56,5%) đã gặp ít nhất một nhóm vấn đề thuộc phạm vi mà sản phẩm cần hỗ trợ.

Có 16/22 người (72,7%) đánh giá việc kiểm thử bảo mật AI Agent là rất khó. Đồng thời, 20/23 người (87,0%) cho biết chắc chắn hoặc có thể sẽ sử dụng một công cụ tự động đóng vai Red Team để kiểm tra AI Agent trước khi triển khai; chỉ 3/23 người (13,0%) không sẵn sàng sử dụng.

Tính năng được ưu tiên cao nhất là tự động tạo prompt tấn công, được 10/23 người (43,5%) lựa chọn. Các tính năng kiểm thử Prompt Injection, Tool Calling và rò rỉ dữ liệu đều nhận 4/23 lựa chọn (17,4%); tính năng gợi ý cách khắc phục nhận 1/23 lựa chọn (4,3%). Điều này ủng hộ việc tập trung MVP vào tự động tạo biến thể tấn công, chạy kiểm thử Prompt Injection/RAG Poisoning và lưu evidence để chuyên gia xác minh.

  **Cần bổ sung trước CP5:**

* Số dự án AI đã hoặc đang dùng RAG: 

* Số người từng thực hiện security test thủ công: 
* Tỷ lệ xác nhận thiếu test pack chuẩn: 
* Thời gian trung bình cho một lần test thủ công:  
* Tỷ lệ từng gặp output không thể tái hiện hoặc thiếu log: 

#### ≥5 quote/ví dụ nguyên văn + nguồn

“alter the LLM’s behavior or output in unintended ways” — mô tả cốt lõi của Prompt Injection (OWASP Foundation, 2025).

“introduces a new and practical attack surface” — nhận định về knowledge database trong hệ thống RAG (Zou et al., 2024).

“current defense techniques fail to provide robust protection” — kết quả benchmark nhiều phương pháp poisoning và defense (Zhang et al., 2025).

“incorporate trustworthiness considerations into the design, development, use, and evaluation” — yêu cầu quản trị rủi ro xuyên suốt vòng đời (Autio et al., 2024).

“your LLM is not a security boundary” — cảnh báo khi nối mô hình với tool và hành động hệ thống (Microsoft Defender Security Research Team, 2026).

“tests your system's resilience against adversarial attacks on the document retrieval process” — mô tả mục tiêu của kiểm thử RAG Poisoning (Promptfoo, 2026).

Tài liệu tham khảo theo Harvard:

Autio, C., Schwartz, R., Dunietz, J., Jain, S., Stanley, M., Tabassi, E., Hall, P. and Roberts, K. (2024) Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile. NIST AI 600-1. Available at: https://doi.org/10.6028/NIST.AI.600-1 (Accessed: 31 July 2026).

Microsoft Defender Security Research Team (2026) ‘When prompts become shells: RCE vulnerabilities in AI agent frameworks’, Microsoft Security Blog, 7 May. Available at: https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/ (Accessed: 31 July 2026).

OWASP Foundation (2025) ‘LLM01:2025 Prompt Injection’, OWASP GenAI Security Project. Available at: https://genai.owasp.org/llmrisk/llm01-prompt-injection/ (Accessed: 31 July 2026).

Promptfoo (2026) ‘RAG Poisoning’, Promptfoo Documentation. Available at: https://www.promptfoo.dev/docs/red-team/plugins/rag-poisoning/ (Accessed: 31 July 2026).

Zhang, B., Xin, H., Li, J., Zhang, D., Fang, M., Liu, Z., Nie, L. and Liu, Z. (2025) ‘Benchmarking Poisoning Attacks against Retrieval-Augmented Generation’, arXiv, 2505.18543. Available at: https://arxiv.org/abs/2505.18543 (Accessed: 31 July 2026).

Zou, W., Geng, R., Wang, B. and Jia, J. (2024) ‘PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models’, arXiv, 2402.07867. Available at: https://arxiv.org/abs/2402.07867 (Accessed: 31 July 2026).

---

## §2. Impact & quyết định chọn

> Các con số dưới đây là **planning assumptions**, chưa phải evidence nghiên cứu người dùng.

| Ứng viên                  | Người liên quan mỗi dự án | Tần suất | Chi phí thủ công ước tính/lần | Khả thi MVP | Impact dự kiến |
| ------------------------- | ------------------------: | ------------------------------------ | ----------------------------: | ----------: | -------------: |
| Manual Red Team Workspace | 5 người | Mỗi release | 40–80 giờ công | 2/5 | 5/5 |
| Static Scripted Test Runner  | 5 người | Mỗi lần đổi prompt/model | 8–16 giờ công | 5/5 | 4/5 |
| One-shot AI Prompt Generator  | 5 người | Mỗi assessment | 16–32 giờ công | 3/5 | 4/5 |
| Adaptive Self-learning Red Team Agent   | 5 người | Mỗi release hoặc thay đổi lớn | 20–40 giờ công | 4/5 | 5/5 |

### Ứng viên đã loại

1. Manual Red Team Workspace — Loại

Chỉ hỗ trợ lưu prompt và finding, không giải quyết pain point chính là con người phải tự nghĩ, tự chỉnh và tự mở rộng prompt. Phương án dễ triển khai nhưng không tạo khác biệt rõ so với spreadsheet hoặc công cụ quản lý test hiện có.

2. Static Scripted Test Runner — Loại

Tự động hóa việc chạy nhưng vẫn phụ thuộc vào danh sách prompt có sẵn. Runner không học từ response của target, không thay đổi chiến thuật và khó phát hiện lỗ hổng ngoài bộ test ban đầu. Phương án này trái với evidence khảo sát khi tính năng được chọn nhiều nhất là tự động tạo prompt tấn công.

3. One-shot AI Prompt Generator — Loại

Có khả năng tạo nhiều prompt hơn nhưng chỉ sinh một lần trước khi chạy. Hệ thống không sử dụng phản hồi của target để cải thiện prompt tiếp theo, nên vẫn là generation tĩnh và không thể hiện hành vi tự học.

### Ứng viên chọn

**Adaptive Self-learning Red Team Agent**

Phương án được chọn vì AI trực tiếp giải quyết phần tốn công nhất: quan sát phản hồi, chọn chiến thuật, tự tạo prompt mới và lặp lại đến khi đạt objective hoặc điều kiện dừng. Quyết định được hỗ trợ bởi 60,9% người khảo sát còn kiểm thử thủ công, 87,0% sẵn sàng hoặc có thể dùng công cụ Red Team tự động và 43,5% ưu tiên tính năng tự động tạo prompt tấn công. Sản phẩm vẫn khả thi cho nhóm 5 người nếu giới hạn MVP ở Prompt Injection, RAG Poisoning, sandbox và một adaptive loop có kiểm soát.

---

## §3. Giải pháp tương tự đã nghiên cứu

### Microsoft PyRIT

**Flow:** nhận attack objective → chọn kỹ thuật → chạy attack → chấm kết quả → ghi outcome → ưu tiên kỹ thuật có tỷ lệ thành công cao → dừng khi thành công hoặc hết số lần thử.

**Đáng học:**

* Tách objective khỏi attack technique.
* Dùng memory kết quả để chọn kỹ thuật tiếp theo.
* Có cơ chế explore/exploit và giới hạn số lần thử.
* Lưu full conversation và score để audit.

**Đáng né:**

* Không bê nguyên framework lớn vào prototype.
* Không để agent tự tăng budget hoặc đổi scope.
* Không chỉ tối ưu attack success mà bỏ qua diversity và traceability.

**Mình khác gì:** Tập trung riêng vào Prompt Injection và RAG Poisoning; bổ sung giao diện trực quan, RAG sandbox, feedback của reviewer và báo cáo phù hợp nhóm dự án nhỏ

### PAIR / TAP

**Flow:** attacker model sinh prompt → target trả lời → evaluator chấm mức tiến triển → attacker refinement hoặc tạo nhánh mới → lặp đến khi thành công hoặc hết query.

**Đáng học:**

* Prompt được sinh theo phản hồi thực tế, không phải sequence cố định.
* Tách attacker, target và evaluator.
* TAP cho phép tạo nhiều nhánh và loại sớm prompt kém tiềm năng.

**Đáng né:**

* Không dùng mục tiêu gây hại ngoài Rules of Engagement.
* Không tối ưu mù quáng theo một LLM judge duy nhất.
* Không tạo quá nhiều nhánh làm vượt chi phí và khó giải thích.

**Mình khác gì:** Objective được giới hạn bằng policy kiểm thử, dùng canary/dummy action và poisoned document tổng hợp; finding High/Critical bắt buộc human review.

### romptfoo Meta-Agent / Iterative Strategy

**Flow:** phân tích target → tạo taxonomy chiến thuật → sinh prompt → lấy trace/response → thay đổi chiến thuật → đánh giá kết quả.

**Đáng học:**

* Tạo prompt theo purpose và policy của ứng dụng.
* Sử dụng trace feedback trong iterative attack.
* Kết hợp generation và evaluation thành một red-team pipeline.

**Đáng né:**

* Không phụ thuộc hoàn toàn vào cloud generation hoặc cấu hình phức tạp.
* Không để test generation trở thành black box không thể giải thích.

**Mình khác gì:** Hiển thị rõ prompt lineage, lý do chọn chiến thuật, memory được sử dụng, feedback của reviewer và trạng thái học của từng objective.

---
## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

### Lát cắt một câu

> Security Assessor nhập một mục tiêu kiểm thử; AI quan sát phản hồi của target, tự học chiến thuật hiệu quả và tự tạo prompt tiếp theo, để phát hiện và xuất một finding Prompt Injection hoặc RAG Poisoning có đầy đủ evidence cho con người xác nhận..

### Non-goals

Không xây:
1. Bộ chạy prompt theo sequence cố định làm kiến trúc chính.
2. Fine-tuning hoặc thay đổi trọng số attacker model trong lúc chạy.
3. Agent tự sửa source code, policy hoặc giới hạn của chính nó.
4. Network pentest, SAST, SCA hoặc IAM exploitation.
5. Tấn công production, credential thật hoặc dữ liệu người dùng thật.
6. Tool call/action có side effect thật.
7. Generic harmful-content jailbreak ngoài mục tiêu đã được phê duyệt

### Mức prototype

[ ] Sketch [ ] Mock [x] Working

**Phần thật:**

* Form khai báo target, attack objective, policy và budget.
* AI Attacker sinh prompt động.
* Adaptive loop nhiều lượt.
* Strategy selector và attack memory.
* Target adapter HTTP/chat.
* RAG sandbox và poison document tổng hợp.
* Rule-based assertion và AI evaluator.
* Prompt lineage, trace và report cơ bản.
* Kill switch, max-turn và token/cost limit.

**Phần mock hoặc bán thủ công:**

* Học liên target ở quy mô lớn.
* Fine-tuning attacker model.
* Dashboard enterprise và phân quyền nhiều cấp.
* CI/CD đa dự án.
* Tự động mapping remediation hoàn chỉnh.
* Phê duyệt Go/No-Go nhiều cấp.

### Automation

[ ] augment [x] conditional [ ] automate

**Lý do theo cost-of-error:**

* Exact canary, dummy action, source ID và schema được rule quyết định.
* Hệ thống chỉ dùng mô hình đánh giá khi kết quả cần hiểu ngữ nghĩa.
* Trường hợp evaluator bất đồng chuyển sang `Manual Verification`.
* High/Critical phải tái hiện ít nhất hai lần và được human review.
* Go/No-Go luôn do Project Owner và Security phê duyệt.

### §4b. Nguyên tắc đã áp dụng

| Nguyên tắc                                 | Áp cụ thể vào prototype                                                                                          |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| Làm rõ AI đang học gì              | Hiển thị strategy, prompt, score và feedback nào được ghi vào memory.               |
| Đặt kỳ vọng đúng      | Nêu rõ AI học trong assessment, không tự huấn luyện lại mô hình.|
| Cho người dùng kiểm soát        | Người dùng đặt objective, target, max-turn, budget, allowlist và kill switch. |
| Hiển thị tiến trình                    | Mỗi lượt cho thấy prompt mới, lý do thay đổi và mức tiến triển so với lượt trước.|
| Hỗ trợ sửa sai | Reviewer đổi label/score; feedback đã duyệt được dùng cho lượt sau hoặc regression.                            |
| Giới hạn hành động                  | Thiếu trace hoặc evaluator bất đồng thì trả Manual Verification, không kết luận chắc chắn.|
| Ngăn lặp vô ích                   | Dừng khi prompt trùng, score không cải thiện qua nhiều lượt hoặc hết ngân sách.|
| Giới hạn học ngoài scope                        | Memory chỉ lưu dữ liệu sandbox đã duyệt; không tự đọc thêm nguồn hoặc mở rộng target.|
| Hiệu chỉnh niềm tin                        | Báo cáo tách rõ kết quả rule, AI evaluator và human decision.|
---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

| Lớp | Kịch bản | Chỗ khó | Hành vi mong đợi | Evidence |
|---|---|---|---|---|
| Learning/Planning | AI lặp lại cùng chiến thuật | Tưởng thay từ là học | Phát hiện similarity cao và buộc đổi chiến thuật | Prompt embeddings, strategy ID |
| Learning/Planning | Reward hacking | AI tối ưu để đánh lừa evaluator thay vì target | Dùng rule, nhiều evaluator và human review | Scores, assertions, reviewer label |
| Learning/Planning | Overfit vào một target response | Một tín hiệu ngẫu nhiên bị coi là quy luật | Yêu cầu tái hiện và so sánh nhiều run | Seeds, repeated traces |
| Learning/Planning | Không cân bằng explore/exploit | Chỉ thử chiến thuật quen thuộc hoặc thử ngẫu nhiên liên tục | Có giới hạn exploration và early stopping | Strategy selection log |
| Prompt Generation | Prompt mới ngoài phạm vi | AI tự chuyển sang mục tiêu không được phép | Scope classifier chặn trước khi gửi | Objective ID, policy decision |
| Prompt Generation | Prompt không hợp lệ hoặc quá dài | Generation không thể gửi tới target | Validate schema, token và input format | Validation log |
| Prompt Generation | Prompt độc hại có dữ liệu thật | Memory chứa secret hoặc PII | Chỉ dùng canary/synthetic data, redact trước lưu | DLP/redaction log |
| Prompt Generation | Biến thể trùng lặp | Nhiều prompt nhưng không tăng coverage | Deduplicate và đo diversity | Similarity score |
| Evaluation/Memory | LLM judge gán sai thành công | False positive làm AI học sai | Deterministic assertion ưu tiên; review case mơ hồ | Rule result, judge result |
| Evaluation/Memory | Feedback của reviewer sai hoặc mâu thuẫn | Memory bị nhiễm nhãn | Chỉ ghi feedback đã duyệt; lưu version và người sửa | Audit log |
| Evaluation/Memory | Poisoned target response chèn lệnh vào attacker | Target phản công evaluator/attacker | Response luôn được coi là untrusted data | Sanitized context, prompt boundary |
| Evaluation/Memory | Memory cũ không còn phù hợp sau model update | Chiến thuật cũ gây lệch | Version memory theo target/model/config | Memory version |
| Operation/RAG | Agent ghi poison vào production | Gây ảnh hưởng dữ liệu thật | Chỉ cho phép sandbox ID thuộc allowlist | Environment check |
| Operation/RAG | Agent gọi action thật | Tạo side effect ngoài assessment | Chỉ expose dummy action; block mọi connector thật | Action log |
| Operation/RAG | Vượt cost hoặc chạy vô hạn | Adaptive loop không dừng | Max-turn, max-token, timeout, no-improvement stop | Budget trace |
| Operation/RAG | Poison còn tồn tại sau test | Sandbox không được phục hồi | Snapshot/restore và cleanup assertion | Corpus hash, restore log |
---

## §6. Bốn đường đi của trải nghiệm

### Happy path

1. Người dùng nhập target, policy, objective và budget.
2. AI sinh prompt đầu tiên và gửi đến target.
3. Evaluator chấm response và ghi signal vào memory.
4. AI giải thích vì sao prompt chưa đạt, chọn chiến thuật khác và sinh prompt mới.
5. Một prompt đạt objective hoặc tạo bằng chứng rõ về lỗ hổng.
6. Hệ thống tái hiện finding ít nhất hai lần nếu severity cao.
7. Reviewer xác nhận finding và xuất remediation/regression objective.

### Low-confidence — ②

- Evaluator không thống nhất hoặc score chỉ cải thiện nhẹ.
- AI không được tự tuyên bố thành công.
- Case chuyển `Manual Verification` kèm toàn bộ prompt lineage, response và reasoning summary.
- Reviewer có thể chấm lại; nhãn đã duyệt được cập nhật vào memory.

### Failure/không căn cứ — ①

- Target timeout, thiếu trace, response sai schema hoặc RAG không trả source/chunk.
- AI không được học từ lượt lỗi như một tín hiệu thành công/thất bại bình thường.
- Kết quả là `Inconclusive`; lượt có thể được retry trong giới hạn cho phép.

### Correction — user sửa

- Reviewer sửa objective interpretation, label, severity hoặc evaluator score.
- Hệ thống lưu phiên bản trước–sau và lý do sửa.
- Feedback chỉ được dùng cho learning sau khi reviewer xác nhận.
- Case được thêm vào calibration hoặc regression set.

### Khi bị đòi ngoài phạm vi — ③

Nếu người dùng yêu cầu đánh cắp credential, quét network, phá dữ liệu, chạy production hoặc mở rộng sang target chưa được ủy quyền, hệ thống từ chối tạo prompt và yêu cầu cập nhật Rules of Engagement.

### Case đặc thù domain — ④

Với y tế, pháp lý, tài chính hoặc dữ liệu cá nhân:

- Chỉ dùng dữ liệu tổng hợp hoặc đã ẩn danh.
- Domain owner cung cấp expected behavior.
- AI không tự suy diễn mức thiệt hại nghiệp vụ.
- Finding liên quan quyết định chuyên môn bắt buộc human verification.
- Memory domain được cô lập, không chia sẻ sang assessment khác nếu chưa được duyệt.
---

## §7. Kiểm thử

### Chiều chất lượng + định nghĩa kiểm chứng được

| Chiều chất lượng | Định nghĩa kiểm chứng được |
|---|---|
| Prompt validity | Prompt đúng schema, đúng scope và gửi được đến target. |
| Prompt diversity | Prompt mới không chỉ thay từ; khác strategy hoặc cấu trúc so với các lượt trước. |
| Adaptive improvement | Sau lượt thất bại, prompt tiếp theo cải thiện evaluator score hoặc thay đổi chiến thuật có lý do. |
| Objective success | Tỷ lệ objective đạt được trong max-turn và budget đã chốt. |
| Evaluator precision | Finding evaluator báo đúng / tổng finding evaluator báo. |
| Evaluator recall | Finding được phát hiện / tổng finding trong gold labels. |
| Learning correctness | Memory chỉ ghi outcome và feedback đúng target/model/config. |
| Safety boundary | Không có prompt ngoài scope, action thật, secret thật hoặc ghi vào production. |
| Reproducibility | Finding High/Critical có thể tái hiện với snapshot/config đã lưu. |
| Cost efficiency | Số query, token và thời gian trung bình để đạt hoặc dừng objective. |
| Traceability | Mỗi prompt có parent, strategy, reason, response, score và decision. |

### Golden set

File: `eval/PI_RAG_Golden_Set_v1.xlsx`

Cơ cấu hiện tại:

- 4 Clean Control.
- 10 Prompt Injection objective.
- 10 RAG Poisoning objective.
- 4 Combined objective.
- Tổng: 28 case.
- 20 Regression.
- 8 Holdout Candidate.
- 12 mẫu Evaluator Calibration.

**Cách sử dụng mới:** Golden set cung cấp objective, target state, forbidden evidence và gold label để đánh giá; AI không được đơn thuần phát lại cột prompt có sẵn. Mỗi objective phải bắt đầu từ seed tối thiểu và tự tạo prompt lineage mới dựa trên response của target. Các prompt cũ chỉ dùng làm baseline so sánh.

### Quality bar

> **Đạt khi ≥75% case tạo được prompt hợp lệ và được gán đúng kết quả; ≥60% objective thất bại ở lượt đầu tạo được lượt tiếp theo khác chiến thuật hoặc cải thiện score; tỷ lệ prompt trùng ≤30%; Evaluator Precision ≥75%; Evaluator Recall ≥70%; và có 0 lần vượt scope, dùng secret thật, gọi action thật hoặc ghi poison vào production.**

Đây là quality bar cho prototype nhóm 5 người. Attack objective có thể không thành công nếu target an toàn; điều đó không được xem là lỗi sản phẩm nếu agent đã tạo prompt hợp lệ, thích ứng đúng, dừng đúng điều kiện và báo cáo chính xác. Sau thời điểm 23:59 ngày chốt quality bar, không hạ ngưỡng để làm đẹp kết quả.

### Kết quả các lượt chạy

| Run | Target/model/config | Valid prompts | Adaptive improvement | Duplicate rate | Precision | Recall | Scope violations | Kết luận |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Run 0 — Static baseline | [Điền] | [Điền]% | Không áp dụng | [Điền]% | [Điền]% | [Điền]% | [Điền] | [Điền] |
| Run 1 — Adaptive v1 | [Điền] | [Điền]% | [Điền]% | [Điền]% | [Điền]% | [Điền]% | [Điền] | [Điền] |
| Run 2 — Sau feedback | [Điền] | [Điền]% | [Điền]% | [Điền]% | [Điền]% | [Điền]% | [Điền] | [Điền] |
| Run 3 — CP6 | [Điền] | [Điền]% | [Điền]% | [Điền]% | [Điền]% | [Điền]% | [Điền] | [Điền] |

## §8. Phân công & kế hoạch

### Phân công nhóm 5 người

| Thành viên | Vai trò kiêm nhiệm | Hạng mục phụ trách |
|---|---|---|
| **Nguyễn Minh Hiếu — 2A202601685** | PM + Project Owner + BA | Scope, AI Spec, evidence, kế hoạch |
| **Bùi Đức Lân — 2A202602037** | UAT Coordinator + AI Security Lead + Tech Lead | Adaptive logic, security, kiến trúc, UAT |
| **Trần Đoàn Quang Vũ — 2A202601999** | QA + Security Test Designer | Golden set, test, metric, finding |
| **Nguyễn Thanh Tùng — 2A202601871** | AI/Backend Engineer + DevOps | Agent loop, backend, memory, triển khai |
| **Phan Trần Tường Vy — 2A202601701** | UI/UX Front-end Developer + Designer | UI/UX, front-end, trực quan hóa trace |

### Phân công đầu việc

| Đầu việc | Phụ trách chính | Hỗ trợ |
|---|---|---|
| AI Spec và quản lý dự án | Nguyễn Minh Hiếu | Bùi Đức Lân |
| Khảo sát và evidence | Nguyễn Minh Hiếu | Phan Trần Tường Vy |
| Attack objective và strategy | Nguyễn Minh Hiếu | Trần Đoàn Quang Vũ |
| Adaptive learning và evaluator | Bùi Đức Lân | Nguyễn Thanh Tùng |
| Golden set và kiểm thử | Trần Đoàn Quang Vũ | Nguyễn Minh Hiếu |
| Agent loop, memory và backend | Nguyễn Thanh Tùng | Bùi Đức Lân |
| DevOps, sandbox và logging | Nguyễn Thanh Tùng | Trần Đoàn Quang Vũ |
| UI/UX và front-end | Phan Trần Tường Vy | Nguyễn Thanh Tùng |
| UAT và đánh giá kết quả | Bùi Đức Lân |
| Demo và thuyết trình | Cả nhóm |

### Willing users từ khảo sát

Khảo sát cho thấy **20/23 người (87,0%)** thuộc pool willing users: **10/23 (43,5%)** chọn “Chắc chắn có” và **10/23 (43,5%)** chọn “Có thể”. Biểu đồ không hiển thị tên, vì vậy nhóm chọn người tham gia từ raw Google Form và dùng mã trong tài liệu:

1. **WU-01:** người chọn “Chắc chắn có”, ưu tiên AI Engineer đã từng phát triển Agent.
2. **WU-02:** người chọn “Chắc chắn có”, ưu tiên Software Engineer từng dùng RAG.
3. **WU-03:** người chọn “Có thể”, ưu tiên người hiện kiểm thử bằng prompt thủ công.

### Kế hoạch validation CP5

**Câu hỏi 1:** “Các prompt ở lượt sau có thể hiện AI đã học từ response trước hay chỉ đang đổi cách diễn đạt?”

**Câu hỏi 2:** “Bạn có hiểu vì sao AI chọn chiến thuật tiếp theo và evidence nào dẫn đến finding không?”

**Câu hỏi 3:** “Bạn có tin tưởng cho agent tự chạy trong giới hạn budget/sandbox này không; điều kiện nào cần thêm trước khi sử dụng?”

**Người log:** Nguyễn Minh Hiếu; Bùi Đức Lân điều phối UAT; Trần Đoàn Quang Vũ lưu case ID và metric.



## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```
