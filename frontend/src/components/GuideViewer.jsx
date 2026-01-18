import React from 'react';
import ReactMarkdown from 'react-markdown';

export default function GuideViewer({ guide }) {
    if (!guide) {
        return (
            <div className="flex-1 flex items-center justify-center bg-slate-50 text-slate-400">
                <p>가이드를 선택해 주세요.</p>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto bg-white p-12">
            <header className="max-w-3xl mx-auto mb-12 border-b border-slate-100 pb-8">
                <h1 className="text-4xl font-extrabold text-slate-900 mb-4">{guide.title}</h1>
                <div className="flex items-center gap-4 text-sm text-slate-500">
                    <span>최종 수정일: {new Date(guide.updatedAt).toLocaleDateString()}</span>
                    <span>•</span>
                    <span>파일: {guide.filePath}</span>
                </div>
            </header>

            <article className="max-w-3xl mx-auto prose prose-slate prose-lg">
                <ReactMarkdown
                    components={{
                        h1: ({ node, ...props }) => <h1 className="text-3xl font-bold mt-8 mb-4 border-b pb-2" {...props} />,
                        h2: ({ node, ...props }) => <h2 className="text-2xl font-semibold mt-6 mb-3" {...props} />,
                        p: ({ node, ...props }) => <p className="mb-4 leading-relaxed text-slate-800" {...props} />,
                        ul: ({ node, ...props }) => <ul className="list-disc pl-6 mb-4 space-y-2" {...props} />,
                        li: ({ node, ...props }) => <li className="text-slate-800" {...props} />,
                        code: ({ node, inline, ...props }) => (
                            <code className={`${inline ? 'bg-slate-100 px-1 rounded' : 'block bg-slate-800 text-slate-100 p-4 rounded-lg my-4'}`} {...props} />
                        ),
                    }}
                >
                    {guide.content}
                </ReactMarkdown>
            </article>
        </div>
    );
}
