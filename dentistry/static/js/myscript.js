// function searchPatient() {
//     var value =  $("#q_disease").val();
//     $.get('/search/patient/' , {
//         value: value,
//     }).then(res => {
//         $("#disease_dev").text(res.diseaseName);
//         $("#id_diseases_0").val(res.diseaseId);
//     });
// }

$(document).ready(function() {
    $('.js-select-q_disease').select2();
});


function searchDisease() {  
    var value = $("#q_disease").val(); // خواندن ورودی کاربر  
    $.get('/search/disease/', { value: value })  
    .then(res => {  
        $("#disease_dev").empty(); // خالی کردن محتوای قبلی  
        $("#id_diseases_0").val(''); // خالی کردن ورودی شناسه  
        
        if (res.length === 0) {  
            $("#disease_dev").text("بیماری پیدا نشد"); // اگر هیچ بیماری پیدا نشد  
        } else {  
            res.forEach(disease => {  
                // ایجاد عنصر برای هر بیماری  
                $("#disease_dev").append(  
                    `<div class="disease-item" data-id="${disease.diseaseId}">  
                        ${disease.diseaseName}  
                    </div>`  
                );  
            });  

            // اضافه کردن رویداد کلیک برای انتخاب بیماری  
            $(".disease-item").click(function() {  
                var selectedId = $(this).data("id");  
                var selectedName = $(this).text();  
                $("#disease_dev").text(selectedName); // نمایش نام انتخاب شده  
                $("#id_diseases_0").val(selectedId); // قرار دادن شناسه انتخاب شده  
            });  
        }  
    })  
    .catch(error => {  
        console.error("Error fetching data:", error); // مدیریت خطاهای شبکه  
        $("#disease_dev").text("خطا در برقراری ارتباط"); // نمایش پیام خطا برای کاربر  
    });  
} 

// function getData() {
//     const id_disease = $("#id_diseases").value(); // Declare variable properly
//     $.ajax({
//         url: '/diseases/res_description/',
//         type: 'GET',
//         data: {
//             id_disease: id_disease,
//         },
//         success: function(response) {
//             console.log('Data received:', response);
//             $('#res_description').html(response); // Use .html() to set the content correctly
//         },
//         error: function(xhr, status, error) {
//             console.error('AJAX Error:', status, error);
//             alert('An error occurred while fetching data. Please try again.'); // User feedback on error
//         }
//     });
// }


// function searchPatient() {  
//     var value =  $("#q_patient").val();
//     $.get('/search/patient/' , {
//         value: value,
//     }).then(res => {
//         $("#patient_table").html(res);
//     });
// }