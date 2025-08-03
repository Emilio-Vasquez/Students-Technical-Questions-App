document.addEventListener('DOMContentLoaded', function () {
    const setupSQLGroup = document.getElementById('setup_sql_group');
    const questionLanguage = window.questionLanguage || 'python';

    if (questionLanguage !== 'sql') {
        setupSQLGroup.style.display = 'none';
        document.getElementById('setup_sql').disabled = true;
    }
});