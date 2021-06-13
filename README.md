# Đếm số hạt gạo trong ảnh:

## Giải pháp chung:

B1, Phân đoạn hình ảnh thành 2 vùng phân biệt;
một vùng đại diện cho hạt gạo - màu trắng, và một vùng đại diện cho nền - màu đen

--> Sử dụng các phương pháp thresholding để convert ảnh về nhị phân

B2, Đếm số lượng đối tượng trắng tinh khiết trong ảnh

## Cụ thể hóa B1:

### Với ảnh gốc và ảnh nhiễu bụi

1. Cái nhìn đầu tiên, với cả 2 ảnh thì chỉ có 3 loại vùng chính được quan tâm, vùng hạt gạo, vùng nền và vùng nhiễu (gồm các đốm nhỏ li ti) --> áp dụng 1 phương pháp smoothing ảnh để có thể giảm nhiễu bước đầu, chúng ta chỉ tập trung vào vùng hạt gạo và vùng nền ảnh.

--> áp dụng một phương pháp làm mờ đơn giản là medianBlur với kích cỡ của kernel là 3 x 3 (con số này đã được tinh chỉnh và chúng tôi thấy 3 x 3 cho kết quả cuối cùng tốt hơn)

Lưu ý: Có thể sử dụng các kỹ thuật blur khác như GaussianBlur, Gamma Correction,...

2. Một nhận xét quan trọng đó là: Ảnh không được chiếu sáng đồng nhất (tức là có vùng tối hơn các vùng khác mặc dù nó có vẻ như cùng một nền giống nhau), vùng trung tâm ảnh sáng nhất, sau đó tối dần về các góc phần tư --> Không thể dùng lấy ngưỡng nhị phân được, vì phương pháp này yêu cầu một ngưỡng cụ thể để quyết định màu của các pixel dựa trên nhỏ hơn hay lớn hơn ngưỡng đó.

--> Giải pháp là cần xác định các ngưỡng khác nhau đối với các phần cụ thể của hình ảnh

--> Sử dụng Local Adaptive Threshold, nó thống kê ngưỡng thích hợp cho mỗi pixel dựa trên hàng xóm lân cận của pixel đó.

3. Sau khi áp dụng threshold method, ảnh thu được là ảnh nhị phân có nền đen, các hạt gạo màu trắng. Tuy nhiên, trong đó vẫn xuất hiện những đốm trắng nhỏ liti trên nền đen, những đốm đen nhỏ liti trên nền trắng. Làm cách nào để loại bỏ chúng ??

--> Sử dụng các toán tử Morphological (chúng là một tập các kernel có thể đạt được nhiều efects khác nhau, như là giảm nhiễu, một số toán tử nhất định rất tốt trong việc giảm thiểu các điểm đen trong nền trắng và ngược lại)

--> áp dụng "xói mòn" (erosion) với ảnh nhị phân

### Với ảnh đen trắng

--> Chỉ cần áp dụng Binary Thresholding

### Với ảnh nhiễu theo chu kỳ

1. Hiện tại với loại ảnh này có một giải pháp khá đơn giản là maximum hóa các columns có nền màu đen --> trắng. Điều này chỉ loại bỏ được một phần nhiễu theo chu kỳ nhưng cũng mang lại tác động lớn

2. Bước tiếp theo ta sẽ sử dụng medianBlur để làm mờ hình ảnh sau khi đã loại nhiễu chu kỳ

3. Đến lúc này ta được ảnh tương đối "sạch" so với ảnh bị nhiễu chu kỳ ban đầu --> có thể áp dụng thresholding, tôi thử nghiệm trên Binary Threholding với phương pháp của Otsu (tính toán thống kê để tự động chọn ngưỡng phù hợp thay vì chọn thủ công bằng tay). Tại sao không sử dụng adaptive thresholding ?? Bởi vì ảnh sau khi đã khử nhiễu chu kỳ khá sáng đều nhau (do phương pháp làm) nên việc sử dụng adaptive thresholding là không cần thiết.

## Cụ thể hóa B2

### Đếm các đối tượng dựa trên các thành phần liên thông

1. Lặp qua toàn bộ các pixel, mỗi khi gặp một pixel trắng

1.1. FloodFill các pixel trắng liền kề --> chung nhãn (gán giá trị mới là một số bắt đầu từ 1 --> những vùng đã fill thì sẽ không phải fill lại nữa), tạo thành 1 phần liên thông

### Đếm các đối tượng dựa trên contours

1. Đầu tiên cần hiểu contours là một đường cong, nó nối tất cả các điểm liên tục (dọc theo một boundary), có cùng màu hoặc cường độ.

2. OpenCV cho chúng ta một bộ đếm Contours được built in.

3. Trong bài toán này, ta cần đếm các hạt gạo màu trắng trong nền đen --> sử dụng EXTERNAL CONTOURS


# Đếm các vật thể thực trong một nền đồng nhất



