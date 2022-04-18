// expandableText
document.querySelectorAll('.expandable-text').forEach(function (expandableText) {
    const expandableTextContent = expandableText.innerHTML.trim().replace(/\s+/g, ' ');
    let displayLimit;
    if (expandableText?.getAttribute("displaylimit") !== null) {
        displayLimit = expandableText.getAttribute("displaylimit");
    } else {
        displayLimit = 220;
    }

    let punctIndexes = [...expandableTextContent.matchAll(new RegExp("[.!?,]", 'gi'))].map(a => a.index);
    let punctIndex = punctIndexes.reduce(function (prev, curr) {
        return (Math.abs(curr - displayLimit) < Math.abs(prev - displayLimit) ? curr : prev);
    }) + 1;
    let spaceIndexes = [...expandableTextContent.matchAll(new RegExp(" ", 'gi'))].map(a => Math.abs(a.index));
    let spaceIndex = spaceIndexes.reduce(function (prev, curr) {
        return (Math.abs(curr - displayLimit) < Math.abs(prev - displayLimit) ? curr : prev);
    });

    // If the distance between the displayLimit and punctuation is more than 25% of the displayLimit, break at the nearest space.
    displayLimit = Math.abs(punctIndex - displayLimit) < (Math.abs(spaceIndex - displayLimit) + 0.25 * displayLimit) ? punctIndex : spaceIndex;

    let textLength = expandableTextContent.length;

    if (displayLimit >= expandableTextContent.length) { return }

    const expandTextToggle = document.createElement('a');
    expandTextToggle.setAttribute('style', 'font-size: 0.8125');
    expandTextToggle.setAttribute('href', '#');
    expandTextToggle.classList.add('inline-link');
    expandTextToggle.innerHTML = 'Read more';
    const expandableTextContentTruncated = expandableTextContent.substring(0, displayLimit) + " (...) ";
    let isTextExpanded = false;

    expandTextToggle.addEventListener('click', function () {
        if (isTextExpanded) {
            expandableText.innerHTML = expandableTextContentTruncated;
            expandableText.blur();
            expandableText.appendChild(expandTextToggle);
            isTextExpanded = false;
            expandTextToggle.innerHTML = 'Read more';
        } else {
            expandableText.innerHTML = expandableTextContent + " ";
            expandableText.appendChild(expandTextToggle);
            expandableText.blur();
            isTextExpanded = true;
            expandTextToggle.innerHTML = 'Read less';
        }
    });

    expandableText.innerHTML = expandableTextContentTruncated;
    expandableText.appendChild(expandTextToggle);
});