interface Props {
  className?: string;
  variant?: "full" | "mark";
}

export function Nadlan3DMark({ className = "", variant = "full" }: Props) {
  if (variant === "mark") {
    return (
      <svg viewBox="0 0 64 32" className={className} aria-label="Nadlan3D">
        <text
          x="0"
          y="24"
          fontFamily="'Frank Ruhl Libre', Georgia, serif"
          fontWeight={500}
          fontSize="22"
          fill="currentColor"
        >
          N
        </text>
        <text
          x="18"
          y="14"
          fontFamily="'Inter Tight', system-ui, sans-serif"
          fontWeight={600}
          fontSize="10"
          fill="var(--color-gold, #9C7A3C)"
          letterSpacing="0.05em"
        >
          3D
        </text>
      </svg>
    );
  }
  return (
    <svg viewBox="0 0 180 36" className={className} aria-label="Nadlan3D">
      <text
        x="0"
        y="26"
        fontFamily="'Frank Ruhl Libre', Georgia, serif"
        fontWeight={500}
        fontSize="26"
        fill="currentColor"
        letterSpacing="-0.01em"
      >
        Nadlan
      </text>
      <text
        x="108"
        y="16"
        fontFamily="'Inter Tight', system-ui, sans-serif"
        fontWeight={600}
        fontSize="12"
        fill="var(--color-gold, #9C7A3C)"
        letterSpacing="0.08em"
      >
        3D
      </text>
      <line x1="0" y1="32" x2="140" y2="32" stroke="currentColor" strokeWidth="0.5" opacity="0.4" />
    </svg>
  );
}
