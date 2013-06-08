function bootstrapCallback(data, form) {
  $.each(data.errors, function(key, val) {
    if (key == '__all__' ) {
        var field_set = $('> fieldset', form);
        field_set.prepend('<div class="alert alert-error">' + val + '</div>');
    } else {
      var field = $('#' + key, form); 
      var field_div = field.parent().parent();
      field_div.addClass("error");
      field.after('<span class="help-inline">' + val + '</span>');
    }
  });
}

function bootstrapRemoveErrorHints(form, type) {
  form.find('div.alert-error').remove();
  form.find('fieldset span.help-inline').remove();
  form.find('fieldset .error').removeClass('error');
}
