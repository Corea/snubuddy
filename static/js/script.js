LanguageMore = function() {
    var $row = $(this).parents('.languageList').clone();
    var delete_button = '<a class="languageRemoveButton btn btn-danger">DELETE</a>';

    $row.find('#LanguageMoreButton').parent().append(delete_button);
    $row.find('#LanguageMoreButton').remove();

    $(this).parents('.languageList').parent().append($row).find(
        '.languageRemoveButton').click(LanguageRemove);

}
LanguageRemove = function() {
    $(this).parents('.languageList').remove();
}

$(document).ready(function() {
    var selector_list = [
        'body.login #NavLogin',
        'body.application #NavApplication',
        'body.matching #NavMatching',
        'body.home #NavHome',
        'body.personal #NavPersonal',
        'body.group #NavGroup',
        'body.team #NavTeam',
        'body.setting #NavSetting',
    ];

    $(selector_list.join()).addClass('active');

    if ($('#LanguageMoreButton').length > 0) {
        $('#LanguageMoreButton').click(LanguageMore);
    }
    if ($('.languageRemoveButton').length > 0) {
        $('.languageRemoveButton').click(LanguageRemove);
    }
});
