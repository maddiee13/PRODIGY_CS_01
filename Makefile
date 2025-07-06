PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
DATADIR ?= $(PREFIX)/share/shiftlock
MANDIR ?= $(PREFIX)/share/man/man1

install:
	@echo "Installing ShiftLock..."
	install -d $(BINDIR)
	install -d $(DATADIR)
	install -d $(MANDIR)
	install -m 755 bin/shiftlock $(BINDIR)/
	install -m 644 src/shiftlock.py $(DATADIR)/
	install -m 644 data/charsets.json $(DATADIR)/
	install -m 644 man/man1/shiftlock.1 $(MANDIR)/
	@echo "Installation complete. Try: shiftlock --help"

uninstall:
	@echo "Removing ShiftLock..."
	rm -f $(BINDIR)/shiftlock
	rm -rf $(DATADIR)
	rm -f $(MANDIR)/shiftlock.1
	@echo "Uninstall complete"