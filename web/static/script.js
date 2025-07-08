const buildURL = (baseURL, params) => {
    const url = new URL(baseURL);
    const searchParams = new URLSearchParams();
    for (const key in params) {
        searchParams.append(key, params[key]);
    }
    url.search = searchParams.toString();
    return url.toString();
};

const escapeHtml = (text) => {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
};

const validateNumericInput = (value) => {
    return value == '' || (! isNaN(parseFloat(value)));
};

const validateDateInput = (value) => {
    if (value === '') {
        return true; // No error if empty
    }
    // Regex to check for yyyy-mm-dd format
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(value)) {
        return false;
    }
    // Attempt to parse the date
    const parts = value.split('-');
    const year = parseInt(parts[0], 10);
    const month = parseInt(parts[1], 10); // Month is 1-indexed in human date, but 0-indexed in Date object
    const day = parseInt(parts[2], 10);
    // Create a Date object. Note: month is 0-indexed for Date constructor
    const dateObj = new Date(year, month - 1, day);
    // Check if the date object is valid AND if its components match the input
    // This catches invalid dates like '2023-02-30' (February 30th)
    return !isNaN(dateObj.getTime()) &&
        dateObj.getFullYear() === year &&
        dateObj.getMonth() === (month - 1) &&
        dateObj.getDate() === day;
};
