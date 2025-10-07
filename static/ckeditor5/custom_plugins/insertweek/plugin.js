import Plugin from '@ckeditor/ckeditor5-core/src/plugin';
import ButtonView from '@ckeditor/ckeditor5-ui/src/button/buttonview';

export default class InsertWeekPlugin extends Plugin {
    init() {
        const editor = this.editor;

        editor.ui.componentFactory.add('insertWeek', locale => {
            const view = new ButtonView(locale);
            view.set({
                label: 'Insert Week Block',
                tooltip: true
            });

            view.on('execute', () => {
                const html = `
<div class="week-block" style="border: 2px solid #007bff; border-radius: 8px; padding: 15px; margin-bottom: 15px;">
    <h3>Week X: Title</h3>
    <h4>Section Title</h4>
    <p>Write section content here...</p>
</div>`;
                editor.model.change(writer => {
                    const viewFragment = editor.data.processor.toView(html);
                    const modelFragment = editor.data.toModel(viewFragment);
                    editor.model.insertContent(modelFragment, editor.model.document.selection);
                });
            });

            return view;
        });
    }
}
