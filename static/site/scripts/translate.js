/** 
 * @file frontend/site/script/translate.js
 * 
 * @author AndreiCristeli
 * 
 * @version 0.2
 */

i18next.init({
    lng: 'pt', // Initial language
    debug: true,
    resources
}, function(err, t) {
    if (document.readyState === 'loading') {
        document.addEventListener("DOMContentLoaded", updateContent);
    } else {
        updateContent();
    }
});

function updateContent() {
    safeTextContent('.diaryText a', i18next.t('diary'));
    safeTextContent('.trueOrFalseText a', i18next.t('trueOrFalse'));
    safeTextContent('.customText a', i18next.t('custom'));

    safeTextContent('.index_question', i18next.t('index_question'));
    safeTextContent('.custom_question', i18next.t('custom_question'));

    const input = document.querySelector('.Input');
    if (input) input.placeholder = i18next.t('inputPlaceholder');

    safeTextContent('.attempts-label', i18next.t('attempts'));

    const labels = document.querySelectorAll('.hint-labels li');
    const keys = [
        'categoryInfoTitle',
        'yearInfoTitle',
        'timeInfoTitle',
        'spaceInfoTitle',
        'structureInfoTitle',
        'solutionInfoTitle',
        'generalityInfoTitle'
    ];

    labels.forEach((el, idx) => {
        if (el) el.textContent = i18next.t(keys[idx]);
    });

    safeTextContent('.howToPlayTitle', i18next.t('howToPlay'));
    safeTextContent('.howToPlayDesc', i18next.t('description'));

    safeTextContent('.categoryTitle', i18next.t('categoryInfoTitle'));
    safeTextContent('.categoryText', i18next.t('categoryInfoText'));

    safeTextContent('.yearTitle', i18next.t('yearInfoTitle'));
    safeTextContent('.yearText', i18next.t('yearInfoText'));

    safeTextContent('.timeTitle', i18next.t('timeInfoTitle'));
    safeTextContent('.timeText', i18next.t('timeInfoText'));

    safeTextContent('.spaceTitle', i18next.t('spaceInfoTitle'));
    safeTextContent('.spaceText', i18next.t('spaceInfoText'));

    safeTextContent('.structureTitle', i18next.t('structureInfoTitle'));
    safeTextContent('.structureText', i18next.t('structureInfoText'));

    safeTextContent('.solutionTitle', i18next.t('solutionInfoTitle'));
    safeTextContent('.solutionText', i18next.t('solutionInfoText'));

    safeTextContent('.generalityTitle', i18next.t('generalityInfoTitle'));
    safeTextContent('.generalityText', i18next.t('generalityInfoText'));
}

// Função auxiliar para evitar erro se o seletor não encontrar o elemento
function safeTextContent(selector, text) {
    const el = document.querySelector(selector);
    if (el) {
        el.textContent = text;
    }
}

export function changeLanguage(lang) {
    i18next.changeLanguage(lang, () => {
        updateContent();
    });
}
