ODIN ?= /opt/homebrew/bin/odin
APP := weck
SRC := weck.odin
BINDIR = $(HOME)/.local/bin

.PHONY: all build strip clean

all: $(BINDIR)/$(APP)

$(BINDIR)/$(APP): $(SRC) Makefile
	$(ODIN) build $(SRC) -file -out:$(APP)
	strip $(APP)
	mv $(APP) $(BINDIR)/$(APP)
	@echo "$(APP) avialable in $(BINDIR)"

clean:
	rm -f $(BINDIR)/$(APP)