$(document).ready(function () {
  document.getElementById("wlcm").click();
  function resize(){
    min_w = $(window).width();
    min_h2 = $(window).height()
    if (min_w <= 991 && min_w >= 441){
        $("#information").css("margin-top", Math.max( (min_h2 - $('#information').height()) / 8 ,20) + "px");
        $("#information").css("margin-bottom", Math.max( (min_h2 - $('#information').height()) / 10, 20) + "px");
        $("#cmnt").css("margin-top", Math.max( (min_h2 - $('#cmnt').height()) / 3 , 20) + "px");
        $("#cmnt").css("margin-bottom", Math.max( (min_h2 - $('#cmnt').height()) / 10, 20) + "px");
    
    }
    else {
      //  $("#information").css("margin-top", Math.max( (min_h2 - $('#information').height()) / 2 , 20) + "px");
      //  $("#information").css("margin-bottom", Math.max( (min_h2 - $('#information').height()) / 2 , 20) + "px");
        $("#cmnt").css("margin-top", Math.max( (min_h2 - $('#cmnt').height()) / 2 , 85) + "px");
        $("#cmnt").css("margin-bottom", Math.max( (min_h2 - $('#cmnt').height()) / 2 , 40) + "px"); 
    }
}
  resize();

  $(window).resize(function () {
    resize();
  });

  var ctx = document.getElementById("myChart").getContext("2d");
  var stackedBar = new Chart(ctx, {
    type: "horizontalBar",
    data: {
      labels: ["Probability"],
      datasets: [
        {
          label: "Negative",
          data: [0.5],
          backgroundColor: "firebrick",
        },
        {
          label: "Positive",
          data: [0.5],
          backgroundColor: "forestgreen",
        },
      ],
    },
    options: {
      tooltips: { enabled: false },
      hover: { mode: null },
      maintainAspectRatio: false,
      legend: {
        labels: {
          fontColor: "white",
        },
      },
      scales: {
        xAxes: [
          {
            barPercentage: 0.1,
            ticks: {
              beginAtZero: true,
              fontFamily: "'Open Sans Bold', sans-serif",
              fontSize: 12,
              fontColor: "#FFF",
              max: 1,
            },
            scaleLabel: {
              display: false,
            },
            stacked: true,
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              fontFamily: "'Open Sans Bold', sans-serif",
              fontSize: 12,
              fontColor: "#FFF",
            },
            stacked: true,
          },
        ],
      },
    },
  });

  counter = 0;
  var request = null;

  $("#txt").keyup(tasks);

  var debounce = _.debounce(afterkeyup, 2000); // Run afterkeyup function, 2 seconds after typing is finished
  function tasks() {
    document.getElementById("run").className = "fas fa-spinner fa-lg  fa-spin";
    if ($("textarea").val().length === 0) {
      document.getElementById("run").className = "far fa-keyboard fa-lg";
      $("#runArea").text("Type your comment!");
    } else {
      $("#runArea").text("Writing ...");
      debounce();
    }
  }

  function afterkeyup() {
    if ($("textarea").val().length === 0) { //Skip for empty comments
      document.getElementById("run").className = "far fa-keyboard fa-lg";
      $("#runArea").text("Type your comment!");
    } else {

      if ($("#runP").hasClass("pleaseShake")) {
        $("#runP").removeClass("pleaseShake");
        $("#pie").removeClass("pleaseShake");
      }

      window.neg = 0;
      window.pos = 0;

      request = $.ajax({
        method: "POST",
        url: "/",
        data: { comment: $("#txt").val() },
        beforeSend: function () {
          if (request != null) { // There are previous requests. Abort previous requests.
            request.abort();
          }
          $("#runArea").text("Processing ...");
        },
      });

      request.done(function (data) {
        window.pos = data["positive"];
        window.neg = data["negative"];
        update(window.pos, window.neg);
        $("#runP").addClass("pleaseShake");
        $("#pie").addClass("pleaseShake");
      });
      request.fail(function () {
        document.getElementById("run").className = "far fa-keyboard fa-lg";
        $("#runArea").text("Type your comment!");
        document.getElementById("error").click();
        $("textarea").val("");
      });
    }
  }

  function update(pos, neg) {
    stackedBar.data.datasets[0].data = [neg];
    stackedBar.data.datasets[1].data = [pos];
    stackedBar.update();
    stackedBar.resize();
    $("#pP").text(pos.toFixed(4));
    $("#pN").text(neg.toFixed(4));

    if (pos > neg) {
      $("#runArea").text("Positive");
      document.getElementById("run").className = "fas fa-smile-beam fa-lg ";
      $("#pP").css("font-size", "large");
      $("#pN").css("font-size", "small");
    } else {
      $("#runArea").text("Negative");
      document.getElementById("run").className = "fas fa-frown-open fa-lg ";
      $("#pP").css("font-size", "small");
      $("#pN").css("font-size", "large");
    }
  }
});
