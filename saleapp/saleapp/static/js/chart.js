function drawChart(type, data, labels, id="myChart", title="# Số lượng") {
    const ctx = document.getElementById(id);

    // Tạo mảng các màu sắc pastel với độ trong suốt tăng lên
    const colors = generatePastelColors(data.length, 0.8);

    new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: title,
                data: data,
                backgroundColor: colors.map(color => color[1]), // Màu nền có độ trong suốt thấp hơn
                borderColor: colors.map(color => color[0]), // Màu viền
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Biểu đồ doanh thu'
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            }
        }
    });
}

// Hàm tạo mảng các màu sắc pastel với độ trong suốt được chỉnh sửa
function generatePastelColors(numColors, alpha) {
    const colors = [];
    const saturation = 60; // Độ bão hòa
    const lightness = 85; // Độ sáng
    const hueStep = 360 / numColors; // Bước màu sắc
    for (let i = 0; i < numColors; i++) {
        const hue = i * hueStep; // Tính toán giá trị màu sắc cho mỗi bước
        const backgroundColor = `hsla(${hue}, ${saturation}%, ${lightness * alpha}%, ${alpha})`; // Màu nền với độ trong suốt thấp hơn
        const borderColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`; // Màu viền
        colors.push([backgroundColor, borderColor]);
    }
    return colors;
}
