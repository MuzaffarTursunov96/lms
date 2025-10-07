document.addEventListener('DOMContentLoaded', function () {
    const syllabusFields = document.querySelectorAll('textarea[id^="id_syllabus_"]');

    syllabusFields.forEach(field => {
        const lang = field.id.split('_').pop();  // uz, ru, en
        field.style.display = 'none';

        const label = document.createElement('h4');
        label.textContent = ``;
        field.parentNode.insertBefore(label, field);

        const container = document.createElement('div');
        container.id = `syllabus-container-${lang}`;
        field.parentNode.insertBefore(container, field.nextSibling);

        const addBtn = document.createElement('button');
        addBtn.textContent = '+ Add Week';
        addBtn.type = 'button';
        addBtn.style = 'margin: 10px 0; background:#0d6efd; color:white; border:none; padding:5px 10px; border-radius:4px;';
        field.parentNode.insertBefore(addBtn, container);

        // Parse existing data
        let data = [];
        try {
            data = JSON.parse(field.value || '[]');
        } catch (e) {
            console.warn('Invalid JSON in ' + field.id);
        }

        function render() {
            container.innerHTML = '';
            data.forEach((week, idx) => {
                const div = document.createElement('div');
                div.className = 'week-block';
                div.style = 'border:1px solid #ccc; padding:10px; margin-bottom:10px; border-radius:8px; background:#f9f9f9;';

                const weekHTML = `
                    <label><b>Week ${idx + 1} Title:</b></label>
                    <input type="text" class="week-title form-control mb-2" value="${week.title || ''}" />
                    <label><b>Description:</b></label>
                    <textarea class="week-desc form-control" style="width:100%; height:150px;">${week.description || ''}</textarea>
                    <button type="button" class="remove-week btn btn-danger mt-2">Remove</button>
                `;
                div.innerHTML = weekHTML;
                container.appendChild(div);

                // Initialize CKEditor on Description field
                const descTextarea = div.querySelector('.week-desc');
                ClassicEditor
                    .create(descTextarea)
                    .then(editor => {
                        editor.model.document.on('change:data', () => {
                            week.description = editor.getData();
                            updateField();
                        });
                    })
                    .catch(error => console.error(error));

                // Handle title changes
                div.querySelector('.week-title').addEventListener('input', e => {
                    week.title = e.target.value;
                    updateField();
                });

                // Handle remove
                div.querySelector('.remove-week').addEventListener('click', () => {
                    data.splice(idx, 1);
                    render();
                    updateField();
                });
            });
        }

        function updateField() {
            field.value = JSON.stringify(data);
        }

        addBtn.addEventListener('click', () => {
            data.push({ title: '', description: '' });
            render();
            updateField();
        });

        render();
    });
});
