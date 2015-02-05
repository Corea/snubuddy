$(document).ready(function() {
    var selector_list = [
        'body.login #NavLogin',
        'body.home #NavHome',
        'body.personal #NavPersonal',
        'body.group #NavGroup',
        'body.team #NavTeam',
        'body.setting #NavSetting',
    ];

    $(selector_list.join()).addClass('active');
});
