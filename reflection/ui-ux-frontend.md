# Reflection cá nhân — UI/UX Frontend

> Họ và tên: _[Bổ sung họ tên và mã học viên trước khi nộp]_

## Vai trò

Tôi phụ trách UI/UX Frontend cho prototype đánh giá an toàn AI/RAG. Mục tiêu của phần tôi làm là biến luồng đánh giá thành một giao diện dễ theo dõi: người dùng cấu hình target, quan sát quá trình chạy test, xem findings và đọc báo cáo tổng hợp.

## Phần việc tôi thực hiện

- Hoàn thiện giao diện cho bốn bước trong Assessment Flow: New Assessment, Test Runner, Findings và Report.
- Thiết kế Sidebar có thanh Progress bốn bước để người dùng luôn biết mình đang ở giai đoạn nào.
- Điều chỉnh hệ thống màu nền và card: nền ảnh được làm tối/mờ hơn, các card thông tin dùng slate đậm để tăng độ tương phản và giúp nội dung dễ đọc.
- Chuẩn hoá typography cho dữ liệu kỹ thuật bằng `JetBrains Mono`, gồm URL API, policy, mô tả profile, loại finding, score và các metric trong report.
- Tinh chỉnh bố cục của New Assessment để card chính có chiều rộng phù hợp hơn với nội dung.

## AI đã hỗ trợ như thế nào

Tôi dùng AI để hỗ trợ rà soát nhanh các component và style đang dùng chung, đề xuất vị trí chỉnh sửa ít ảnh hưởng nhất, và hỗ trợ viết các thay đổi Vue/Tailwind. Sau mỗi thay đổi, tôi kiểm tra lại diff và chạy build Vite để phát hiện lỗi biên dịch.

AI giúp tôi tăng tốc các thao tác lặp lại, nhưng tôi vẫn tự quyết định các điểm UX như mức độ tương phản, phạm vi áp dụng style, font cho dữ liệu kỹ thuật và bố cục của các card. Tôi có thể giải thích được các thay đổi ở `App.vue`, `style.css`, Sidebar và các view trong Assessment Flow.

## Một case chưa tốt và bài học rút ra

Ban đầu tôi truyền utility class font vào component input để đổi font của URL Target API. Tuy nhiên, ô input vẫn không đổi như mong muốn vì rule `.cyber-input` đặt `font-family` có độ ưu tiên và thứ tự ghi đè cao hơn. Tôi đã kiểm tra lại nguyên nhân, sau đó tạo class CSS riêng `.cyber-input--jetbrains` gắn trực tiếp với input.

Bài học của tôi là không chỉ dựa vào utility class khi làm việc với component có style nền. Cần kiểm tra cascade CSS, độ ưu tiên selector và thứ tự load style; khi một kiểu trình bày là yêu cầu quan trọng, nên tạo class mang ý nghĩa rõ ràng và kiểm chứng trực tiếp trên giao diện.

## Điều tôi muốn cải thiện

Nếu có thêm thời gian, tôi sẽ thực hiện thêm user test ngắn với các thành viên không trực tiếp code để đo khả năng hiểu luồng bốn bước, đặc biệt là trạng thái Progress và khả năng đọc dữ liệu trong màn Report. Tôi cũng sẽ bổ sung kiểm thử responsive cho kích thước màn hình nhỏ trước khi demo.
