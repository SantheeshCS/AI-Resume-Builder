function getCSRFToken() {
    const el = document.querySelector('meta[name="csrf-token"]');
    if (el) return el.getAttribute('content');
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
        c = c.trim();
        if (c.startsWith(name + '=')) {
            return decodeURIComponent(c.substring(name.length + 1));
        }
    }
    return '';
}

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('resume-form');
    const autosaveStatus = document.getElementById('autosave-status');
    const csrfToken = getCSRFToken();

    if (form && autosaveStatus) {
        let timeoutId = null;
        form.addEventListener('input', () => {
            autosaveStatus.textContent = 'Saving...';
            if (timeoutId) clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                const url = window.location.pathname.replace('/edit/', '/autosave/');
                const formData = new FormData(form);
                fetch(url, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': csrfToken },
                    body: formData
                }).then(r => r.json()).then(data => {
                    if (data.status === 'ok') {
                        autosaveStatus.textContent = 'Auto-saved';
                    } else {
                        autosaveStatus.textContent = 'Autosave error';
                    }
                }).catch(() => {
                    autosaveStatus.textContent = 'Autosave failed';
                });
            }, 800);
        });
    }

    const summaryBtn = document.getElementById('ai-summary-btn');
    const expBtn = document.getElementById('ai-experience-btn');
    const kwBtn = document.getElementById('ai-keywords-btn');

    function postAI(url, payload, cb) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: new URLSearchParams(payload)
        }).then(r => r.json()).then(cb).catch(() => alert('AI request failed'));
    }

    if (summaryBtn) {
        summaryBtn.addEventListener('click', () => {
            const rid = summaryBtn.dataset.resume;
            const job = document.getElementById('id_job_title').value;
            const skills = document.getElementById('id_skills').value;
            const years = '1';
            const url = `/resume/${rid}/ai/summary/`;
            postAI(url, { job_title: job, skills: skills, years: years }, data => {
                if (data.summary) {
                    document.getElementById('id_summary').value = data.summary;
                }
            });
        });
    }

    if (expBtn) {
        expBtn.addEventListener('click', () => {
            const rid = expBtn.dataset.resume;
            const job = document.getElementById('id_job_title').value;
            const exp = document.getElementById('id_experience').value;
            const url = `/resume/${rid}/ai/experience/`;
            postAI(url, { job_title: job, experience: exp }, data => {
                if (data.experience) {
                    document.getElementById('id_experience').value = data.experience;
                }
            });
        });
    }

    if (kwBtn) {
        kwBtn.addEventListener('click', () => {
            const rid = kwBtn.dataset.resume;
            const job = document.getElementById('id_job_title').value;
            const skills = document.getElementById('id_skills').value;
            const url = `/resume/${rid}/ai/keywords/`;
            postAI(url, { job_title: job, skills: skills }, data => {
                if (data.keywords) {
                    const sField = document.getElementById('id_skills');
                    sField.value = sField.value + '\\n' + data.keywords;
                }
            });
        });
    }
});
