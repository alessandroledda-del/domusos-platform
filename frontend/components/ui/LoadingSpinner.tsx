import clsx from 'clsx'

interface LoadingSpinnerProps {
  className?: string
  label?: string
}

export function LoadingSpinner({ className, label = 'Loading...' }: LoadingSpinnerProps) {
  return (
    <div className={clsx('flex items-center justify-center gap-3', className)} role="status" aria-live="polite">
      <div className="h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600 dark:border-slate-700 dark:border-t-blue-400" />
      <span className="text-sm text-slate-600 dark:text-slate-300">{label}</span>
    </div>
  )
}
