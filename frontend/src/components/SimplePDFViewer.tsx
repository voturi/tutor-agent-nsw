'use client';

import { useState, useEffect } from 'react';
import { FileText, Download, ExternalLink } from 'lucide-react';

interface SimplePDFViewerProps {
  file: File | string | null;
  className?: string;
}

export default function SimplePDFViewer({ file, className = '' }: SimplePDFViewerProps) {
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!file) {
      setPdfUrl(null);
      return;
    }

    if (file instanceof File) {
      setIsLoading(true);
      console.log('SimplePDFViewer: Creating object URL for file:', file.name);
      
      try {
        const url = URL.createObjectURL(file);
        setPdfUrl(url);
        setError(null);
        setIsLoading(false);
        console.log('SimplePDFViewer: Object URL created successfully');
        
        // Cleanup function
        return () => {
          URL.revokeObjectURL(url);
          console.log('SimplePDFViewer: Object URL revoked');
        };
      } catch (err) {
        console.error('SimplePDFViewer: Failed to create object URL:', err);
        setError('Failed to load PDF file');
        setIsLoading(false);
      }
    } else if (typeof file === 'string') {
      setPdfUrl(file);
      setError(null);
    }
  }, [file]);

  const handleDownload = () => {
    if (pdfUrl && file instanceof File) {
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = file.name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleOpenInNewTab = () => {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    }
  };

  if (!file) {
    return (
      <div className={`flex items-center justify-center bg-background border border-custom rounded-lg min-h-[300px] ${className}`}>
        <div className="text-center text-muted p-8">
          <FileText className="w-12 h-12 mx-auto mb-3 text-muted" />
          <p className="text-sm">No PDF file selected</p>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className={`flex items-center justify-center bg-background border border-custom rounded-lg min-h-[300px] ${className}`}>
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
          <p className="text-sm text-muted">Loading PDF...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`flex items-center justify-center bg-background border border-custom rounded-lg min-h-[300px] ${className}`}>
        <div className="text-center text-red-500 p-8">
          <FileText className="w-12 h-12 mx-auto mb-3" />
          <p className="text-sm mb-3">{error}</p>
          <button
            onClick={() => {
              setError(null);
              setIsLoading(true);
            }}
            className="text-xs text-primary hover:underline"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex flex-col bg-background border border-custom rounded-lg ${className}`}>
      {/* PDF Controls */}
      <div className="flex items-center justify-between p-3 border-b border-custom bg-surface shrink-0">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-primary" />
          <span className="text-sm font-medium text-foreground truncate">
            {file instanceof File ? file.name : 'PDF Document'}
          </span>
        </div>
        
        <div className="flex items-center gap-2">
          {file instanceof File && (
            <button
              onClick={handleDownload}
              className="p-1 rounded hover:bg-background text-muted hover:text-foreground"
              title="Download PDF"
            >
              <Download className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={handleOpenInNewTab}
            className="p-1 rounded hover:bg-background text-muted hover:text-foreground"
            title="Open in new tab"
          >
            <ExternalLink className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* PDF Display */}
      <div className="flex-1 p-2 min-h-0">
        {pdfUrl ? (
          <iframe
            src={`${pdfUrl}#toolbar=1&navpanes=1&scrollbar=1`}
            className="w-full h-full min-h-[300px] border border-custom rounded"
            title="PDF Viewer"
            onLoad={() => console.log('SimplePDFViewer: PDF iframe loaded')}
            onError={(e) => {
              console.error('SimplePDFViewer: PDF iframe error:', e);
              setError('Failed to display PDF');
            }}
          />
        ) : (
          <div className="flex items-center justify-center h-[400px] bg-gray-50 border border-custom rounded">
            <div className="text-center text-muted">
              <FileText className="w-12 h-12 mx-auto mb-3" />
              <p className="text-sm">PDF not available</p>
            </div>
          </div>
        )}
      </div>

      {/* PDF Info */}
      {file instanceof File && (
        <div className="p-2 border-t border-custom bg-surface shrink-0">
          <div className="text-xs text-muted text-center">
            {file.name} • {Math.round(file.size / 1024)}KB
          </div>
        </div>
      )}
    </div>
  );
}
