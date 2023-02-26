function upload() {
  console.log("Uploaded");
  var formData = new FormData($("#upload_form")[0]);
  console.log(formData);
  $.ajax({
    url: "{% url 'view' %}",
    type: "POST",
    data: formData,
    success: function (data) {
      $(".error").remove();
      //console.log(data);

      if (data.error) {
        alert(data.error);
      } else {
        console.log("Success");
        window.alert("Your File is uploaded");
        window.location.href = "{% url 'view' %}";
      }
    },
    error: function (data) {
      console.log("Error occured");
    },
    cache: false,
    contentType: false,
    processData: false,
  });
}
