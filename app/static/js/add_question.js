document.addEventListener('DOMContentLoaded', function () {
    const langSelect = document.getElementById('language');
    const funcSigGroup = document.getElementById('function_signature_group');
    const funcSigInput = document.getElementById('function_signature');

    function toggleFuncSig() {
        if (langSelect.value === 'sql') {
            funcSigGroup.style.display = 'none';
            funcSigInput.disabled = true;
        } else {
            funcSigGroup.style.display = 'block';
            funcSigInput.disabled = false;
        }
    }

    langSelect.addEventListener('change', toggleFuncSig);
    toggleFuncSig(); // Run once on load
});