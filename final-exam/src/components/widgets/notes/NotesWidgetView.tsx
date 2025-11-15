import { useRef } from 'react';
import type { NotesWidget } from '../../../types';
import { useWorkspaceStore } from '../../../state/useWorkspaceStore';

interface Props {
  widget: NotesWidget;
}

const exec = (command: string) => document.execCommand(command, false);

export function NotesWidgetView({ widget }: Props) {
  const updateContent = useWorkspaceStore((s) => s.updateNotesContent);
  const ref = useRef<HTMLDivElement>(null);

  const handleInput = () => {
    updateContent(widget.id, ref.current?.innerHTML ?? '');
  };

  return (
    <div className="notes-widget">
      <div className="notes-toolbar" role="toolbar" aria-label="Formatting">
        <button onClick={() => exec('bold')} aria-label="Bold">
          B
        </button>
        <button onClick={() => exec('italic')} aria-label="Italic">
          I
        </button>
        <button onClick={() => exec('insertUnorderedList')} aria-label="Bullets">
          •
        </button>
      </div>
      <div
        ref={ref}
        className="notes-editor"
        contentEditable
        suppressContentEditableWarning
        onInput={handleInput}
        dangerouslySetInnerHTML={{ __html: widget.config.content }}
        aria-label="Notes editor"
      />
    </div>
  );
}
