(function($) {
    function inputs(form)   {
        //return form.find("input, select, textarea")
        return form.find(":input:visible:not(:button)");
    }
    function removeErrorHints(form, type) {
        //p
        form.find('ul.errorlist').remove();
        //table
        inputs(form).prev('ul.errorlist').remove();
        form.find('tr:has(ul.errorlist)').remove();
        //ul
        inputs(form).prev().prev('ul.errorlist').remove();
        form.find('li:has(ul.errorlist)').remove();
    }

    $.fn.djangoajaxform = function(settings) {
        settings = $.extend({
            type: 'table',
            onValidateSucc: function(data, form){},
            onValidateFail: function(data, form){},
            callback: false,
            fields: false,
            dom: this,
            onStart:function(op){return true;},
            onComplete:function(op){},
            removeErrorHints: removeErrorHints,
            event: 'submit',
            pureAjax: true,
            submitHandler: null
        }, settings);

        return this.each(function() {
            var form = $(this);
            settings.dom.bind(settings.event, function()  {
                var status = false;
                var data = form.serialize();
                if (settings.fields) {
                    data += '&' + $.param({fields: settings.fields});
                }
                var url = form.attr('action');
                $.ajax({
                    async: false,
                    data: data,
                    dataType: 'json',
                    traditional: true,
                    error: function(XHR, textStatus, errorThrown)   {
                        status = true;
                    },
                    beforeSend: function(){
                        return settings.onStart(settings);
                    },
                    complete: function(){
                        settings.onComplete(settings);
                    },
                    success: function(data, textStatus) {
                        status = data.valid;
                        settings.removeErrorHints(form, settings.type);
                        if (!status) {
                            if (settings.callback)  {
                                settings.callback(data, form);
                            }
                            else    {
                                var get_form_error_position = function(key) {
                                    key = key || '__all__';
                                    if (key == '__all__') {
                                        var filter = ':first';
                                    } else {
                                        var filter = ':first[id^=id_' + key.replace('__all__', '') + ']';
                                    }
                                    return inputs(form).filter(filter).parent();
                                };
                                if (settings.type == 'p')    {
                                    $.each(data.errors, function(key, val)  {
                                        if (key.indexOf('__all__') >= 0)   {
                                            var error = get_form_error_position(key);
                                            if (error.prev().is('ul.errorlist')) {
                                                error.prev().before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                            }
                                            else    {
                                                error.before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                            }
                                        }
                                        else    {
                                            $('#' + key, form).parent().before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                        }
                                    });
                                }
                                if (settings.type == 'table')   {
                                    $.each(data.errors, function(key, val)  {
                                        if (key.indexOf('__all__') >= 0)   {
                                            get_form_error_position(key).parent().before('<tr><td colspan="2"><ul class="errorlist"><li>' + val + '.</li></ul></td></tr>');
                                        }
                                        else    {
                                            $('#' + key, form).before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                        }
                                    });
                                }
                                if (settings.type == 'ul')  {
                                    $.each(data.errors, function(key, val)  {
                                        if (key.indexOf('__all__') >= 0)   {
                                            get_form_error_position(key).before('<li><ul class="errorlist"><li>' + val + '</li></ul></li>');
                                        }
                                        else    {
                                            $('#' + key, form).prev().before('<ul class="errorlist"><li>' + val + '</li></ul>');
                                        }
                                    });
                                }
                            }
                            settings.onValidateFail(data, form);
                        } else {
                            settings.onValidateSucc(data, form);
                        }
                    },
                    type: 'POST',
                    url: url
                });
                if (status && settings.submitHandler) {
                    return settings.submitHandler.apply(this);
                }
                if (settings.pureAjax) return false
                return status;
            });
        });
    };
})(jQuery);
