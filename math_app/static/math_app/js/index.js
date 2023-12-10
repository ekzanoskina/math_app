$(document).ready(function(){

//запрещает вводить любые символы кроме цифр в поле integerfield
$(':input[type="number"]').on('keypress', function (e) {
   if (String.fromCharCode(e.keyCode).match(/[^0-9]/g)) return false;
    var reg = /^0+/g;
    if (this.value.match(reg)) {
        this.value = this.value.replace(reg, '');
    }
});

//Checkboxes, general variables

var short_ans_qs = $('.accordion.short-answer-questions')
var detailed_ans_qs = $('.accordion.detailed-answer-questions')
var $short_answer = $('#short-answer')
var $detailed_answer = $('#detailed-answer')

function select_all_qs_in_part(part, questions){
part.on('click', function() {
  if ($(this).is(':checked')) {
      questions.find('.check').prop('checked', true);
      questions.find('input[type="number"]').val(1);
      questions.find('.check-all').prop('checked', true);
  } else {
      questions.find('.check').prop('checked', false);
      questions.find('input[type="number"]').val(0);
      questions.find('.check-all').prop('checked', false);
  };
  calculateSum();
  });

questions.on('change click keyup input paste blur', function(){


  var $inputs = questions.find('input[type="number"]');
  var allValuesGreaterThanZero = true;

  $inputs.each(function() {
    var value = parseInt($(this).val());
    if (isNaN(value) || value <= 0) {
      allValuesGreaterThanZero = false;
      return false; // Exit the loop early if any value is not greater than zero
    }
  });

  part.prop('checked', allValuesGreaterThanZero);
})
}


select_all_qs_in_part($short_answer, short_ans_qs)
select_all_qs_in_part($detailed_answer, detailed_ans_qs)

// checkboxes


$('input[type=number]').on('click',function(){ this.select(); });

$('.check-all').parents('.accordion-item').find('.number-input').on('propertychange change click keyup input paste blur', function(){

  var value = parseInt($(this).find(':input[type="number"]').val())
  var check_all = $(this).parents('.accordion-item').find('.check-all')
  if (value > 0 && $(this).parents('.accordion-item').find('.check:checked').length == 0)
  {
  check_all.prop('checked', 'checked');
  $(this).parents('.accordion-item').find('.check').each(function() {
      this.checked = true;
    })
    };
    if (!value ) {
    check_all.prop('checked', false);
    $(this).parents('.accordion-item').find('.check').each(function() {
      this.checked = false;
    });
  }
  });

$('.check-all').on('click', function() {

  if (this.checked) {
    $(this).parents('.accordion-body').find('.check').each(function() {

      this.checked = true;
      $(this).parents('.accordion-item').find(':input[type="number"]').val(1)
    });
  } else {
    $(this).parents('.accordion-body').find('.check').each(function() {
      this.checked = false;
      $(this).parents('.accordion-item').find(':input[type="number"]').val(0)

    });
  };
  calculateSum()
});

//".checkbox" change
$('.check-all').parents('.accordion-body').find('.check').change(function(){
	//uncheck "select all", if one of the listed checkbox item is unchecked
    if(false == $(this).prop("checked")){ //if this item is unchecked
        $(this).parents('.accordion-body').find('.check-all').prop('checked', false); //change "select all" checked status to false
    }
  var $parent = $(this).parents('.accordion-body'),
    $inner = $parent.find(".check"),
    $checked = $parent.find(".check:checked"),
    $outer = $parent.find(".check-all"),
    chk = $inner.length === $checked.length ? this.checked : false;
  $outer.prop("checked", chk)

});

$('.number-input').parents('.accordion-item').find('.check').on('change click keyup input paste blur', function(){

   var value = $(this).parents('.accordion-item').find(':input[type="number"]').val()
   if(($(this).prop("checked")  ) && (value == '' || value == 0)){
        $(this).parents('.accordion-item').find(':input[type="number"]').val(1)

}
    if(($(this).parents('.accordion-item').find('.check:checked').length == 0) && (value > 0)){
    $(this).parents('.accordion-item').find(':input[type="number"]').val(0)
    }
    calculateSum();
});
// склонение существительных - кнопка "составить вариант из x заданий"
function num_word(value, words){
	value = Math.abs(value) % 100;
	var num = value % 10;
	if(value > 10 && value < 20) return words[2];
	if(num > 1 && num < 5) return words[1];
	if(num == 1) return words[0];
	return words[2];
};

        //iterate through each textboxes and add keyup
        //handler to trigger sum event
   $('.number-input').each(function() {

            $(this).on('change click keyup input paste blur', function(){
                calculateSum();
            });
        });

    function calculateSum() {

        var sum = 0;
        //iterate through each textboxes and add the values
        $('.cat_quantity').each(function(i, el) {
        // если выбрана категория "первые 5 номеров", то увеличивать счетчик на 5
            if ( i == 0) {
            var value = $(this).val() * 5
            }
            else
            {var value = $(this).val()}
            //add only if the value is number
            if(value.length!=0 && parseInt(value) != 0) {
                sum += parseInt(value);
            }
        });
        if(sum != 0) {
        $('#your_variant_exam').prop('disabled', false)
        $("#sum").html('из ' + sum + " " + num_word(sum, ['задания', 'заданий', 'заданий']));
}
        else {
        $("#sum").html('')
        $('#your_variant_exam').prop('disabled', true)
        }
};
  });




// ТАЙМЕР
  var startTime = 0;
    elapsed = 0,
    timerId = 0,
    $timer = $("#timer");

  function formatTime(time) {
    var hrs = Math.floor(time / 60 / 60 / 1000),
      min = Math.floor((time - hrs * 60 * 60 * 1000) / 60 / 1000),
      sec = Math.floor((time - hrs * 60 * 60 * 1000 - min * 60 * 1000) / 1000);

    hrs = hrs < 10 ? "0" + hrs : hrs;
    min = min < 10 ? "0" + min : min;
    sec = sec < 10 ? "0" + sec : sec;

    return hrs + ":" + min + ":" + sec;
  }

  function elapsedTimeFrom(time) {
    return formatTime(time - startTime + elapsed);
  }

  function showElapsed() {
    $timer.text(elapsedTimeFrom(Date.now()));
  }


  function startTimer() {
    startTime = localStorage.getItem('startTime') || Date.now();

    timerId = timerId || setInterval(showElapsed, 10);
    localStorage.setItem('startTime',startTime);
    }

  function pauseTimer() {
    // React only if timer is running
    if (timerId) {
      clearInterval(timerId);
      elapsed += Date.now() - startTime;
      startTime = 0;
      timerId = 0;
    }
  }

  function resetTimer() {
    clearInterval(timerId);
    localStorage.removeItem('startTime')
    $timer.text("00:00:00");
    startTime = 0;
    elapsed = 0;
    timerId = 0;
  }


  function setElapsed() {
    var time = $timer.text(),
      arr = time.split(":");
    elapsed = parseInt(arr[0] * 60 * 60, 10);
    elapsed += parseInt(arr[1] * 60, 10);
    elapsed += parseInt(arr[2], 10);
    elapsed *= 1000;
  }

  function sendTime() {
    pauseTimer();
    // Set hidden input value before send
    $("[name='time']").val(formatTime(elapsed));
    localStorage.removeItem('startTime');
  }
//  запуск нового таймера каждый раз, когда ученик начинает экзамен
  $(window).on('load', startTimer);
//  (по готовому)
  $('#variant_exam').on('click', resetTimer)
//  (по своему варианту)
  $('#your_variant_exam').on('click', resetTimer)
//  сохранение значения таймера в hidden input
  $("form").submit(sendTime)

// конец таймера

// выпадающие списки для заданий, решений и критериев

$(document).ready(function(){
$(".toggle_container").hide();
$("button.reveal.solution").click(function(){
    $(this).toggleClass("active").next().slideToggle("fast");

    if ($.trim($(this).text()) === 'Показать решение') {
        $(this).text('Спрятать решение');
    } else {
        $(this).text('Показать решение');
    }

    return false;
});
 $("a[href='" + window.location.hash + "']").parent(".reveal.solution").click();
});

$(document).ready(function(){
$(".toggle_container").hide();
$("button.reveal.criteria").click(function(){
    $(this).toggleClass("active").next().slideToggle("fast");

    if ($.trim($(this).text()) === 'Показать критерии') {
        $(this).text('Спрятать критерии');
    } else {
        $(this).text('Показать критерии');
    }

    return false;
});
 $("a[href='" + window.location.hash + "']").parent(".reveal.criteria").click();
});

$(document).ready(function(){
$(".toggle_container").hide();
$(".reveal.tests").click(function(){
    $(this).toggleClass("active").next().slideToggle("fast");

    if ($.trim($(this).text()) === 'Показать задания') {
        $(this).text('Спрятать задания');
    } else {
        $(this).text('Показать задания');
    }

    return false;
});
 $("a[href='" + window.location.hash + "']").parent(".reveal.tests").click();
});

$('table').wrap('<div class="table-responsive"></div>');

$(document).ready(function(){
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}
})
