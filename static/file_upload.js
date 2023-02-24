
$("#upload_form").submit(function (e) {
  // preventing from page reload and default actions
  e.preventDefault();
  // serialize the data for sending the form data.
  // var serializedData = $(this).serialize();
  var form_data = new FormData();

      for (var x = 0; x < ins; x++) {
        form_data.append(
          "files[]",
          document.getElementById("multiFiles").files[x]
        );
        console.log("file uploading");
  // make POST ajax call
  $.ajax({
    type: "POST",
    url: "{% url 'view' %}",
    data: serializedData,
    success: function (response) {
      // on successfull creating object
      // 1. clear the form.
      $("#upload_form").trigger("reset");
      console.log("success");
    },
    error: function (response) {
      // alert the error if any error occured
      alert("Error in upload");
    },
  });
});




// $(document).ready(function (e) {
//   $("#upload").on("click", function () {
//     var form_data = new FormData();
//     var ins = document.getElementById("multiFiles").files.length;

//     if (ins == 0) {
//       $("#msg").html('<span style="color:red">Select at least one file</span>');
//       console.log("No files uploaded");
//       return;
//     }

//     for (var x = 0; x < ins; x++) {
//       form_data.append(
//         "files[]",
//         document.getElementById("multiFiles").files[x]
//       );
//       console.log("file uploading");
//     }

//     csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

//     //console.log(csrf_token);

//     form_data.append("csrfmiddlewaretoken", csrf_token);

//     $.ajax({
//       url: "upload", // point to server-side URL
//       dataType: "json", // what to expect back from server
//       cache: false,
//       contentType: false,
//       processData: false,
//       //data: {'data': form_data, 'csrfmiddlewaretoken': csrf_token},
//       data: form_data,
//       type: "post",
//       success: function (response) {
//         // display success response
//         $("#msg").html(response.msg);
//         console.log("SUCessfully uploaded");
//       },
//       error: function (response) {
//         $("#msg").html(response.message); // display error response
//         console.log("Error in uploading");
//       },
//     });
//   });
// });