import AppKit

let inputPath = CommandLine.arguments.count > 1
  ? CommandLine.arguments[1]
  : "../frames/01-needs-owner.png"
let outputPath = CommandLine.arguments.count > 2
  ? CommandLine.arguments[2]
  : "lineage-relay-devpost-cover.png"

guard let source = NSImage(contentsOfFile: inputPath) else {
  fputs("Unable to read source image: \(inputPath)\n", stderr)
  exit(1)
}

let canvasSize = NSSize(width: 1200, height: 630)
let image = NSImage(size: canvasSize)
image.lockFocus()

NSColor(red: 0.937, green: 0.957, blue: 0.945, alpha: 1).setFill()
NSBezierPath(rect: NSRect(origin: .zero, size: canvasSize)).fill()

NSColor(red: 0.247, green: 0.463, blue: 0.427, alpha: 1).setFill()
NSBezierPath(rect: NSRect(x: 70, y: 540, width: 12, height: 12)).fill()

func text(_ value: String, x: CGFloat, y: CGFloat, size: CGFloat, weight: NSFont.Weight, color: NSColor) {
  let attributes: [NSAttributedString.Key: Any] = [
    .font: NSFont.systemFont(ofSize: size, weight: weight),
    .foregroundColor: color,
  ]
  value.draw(at: NSPoint(x: x, y: y), withAttributes: attributes)
}

let ink = NSColor(red: 0.09, green: 0.15, blue: 0.16, alpha: 1)
let muted = NSColor(red: 0.25, green: 0.32, blue: 0.33, alpha: 1)
text("LINEAGE RELAY", x: 70, y: 485, size: 52, weight: .bold, color: ink)
text("Schema-change review grounded in", x: 70, y: 405, size: 27, weight: .regular, color: muted)
text("DataHub lineage, ownership, and governance.", x: 70, y: 367, size: 27, weight: .regular, color: muted)

NSColor(red: 0.94, green: 0.88, blue: 0.64, alpha: 1).setFill()
NSBezierPath(roundedRect: NSRect(x: 70, y: 195, width: 430, height: 65), xRadius: 4, yRadius: 4).fill()
text("NEEDS OWNER", x: 94, y: 215, size: 27, weight: .bold, color: ink)
text("Evidence before a false green light.", x: 70, y: 135, size: 23, weight: .regular, color: muted)

NSColor(red: 0.09, green: 0.15, blue: 0.16, alpha: 0.14).setFill()
NSBezierPath(roundedRect: NSRect(x: 692, y: 18, width: 476, height: 570), xRadius: 8, yRadius: 8).fill()
source.draw(in: NSRect(x: 680, y: 30, width: 476, height: 570), from: .zero, operation: .sourceOver, fraction: 1)

image.unlockFocus()
guard let tiff = image.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: tiff),
      let png = bitmap.representation(using: .png, properties: [:]) else {
  fputs("Unable to encode PNG.\n", stderr)
  exit(1)
}
try png.write(to: URL(fileURLWithPath: outputPath))
