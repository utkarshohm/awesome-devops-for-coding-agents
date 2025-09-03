# Cursor AI Safety Shell Protection
# Source this file in your .bashrc or .zshrc to add real command protection
# This provides actual enforcement at the shell level for Cursor and terminal usage

# Color codes for messages
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==============================================================================
# GIT PROTECTION - Prevent accidental commits of sensitive files
# ==============================================================================
git() {
    # Block dangerous git add commands
    if [[ "$1" == "add" ]]; then
        if [[ "$2" == "." || "$2" == "-A" || "$2" == "--all" ]]; then
            echo -e "${RED}🚫 Blocked: 'git add $2'${NC}"
            echo -e "${YELLOW}💡 This can accidentally commit sensitive files like:${NC}"
            echo "   • .env files with API keys"
            echo "   • Private keys and certificates"
            echo "   • Local config with passwords"
            echo ""
            echo -e "${GREEN}✅ Safe alternatives:${NC}"
            echo "   • git add *.py                    # Add only Python files"
            echo "   • git add -p                      # Interactive staging"
            echo "   • git add src/                    # Add specific directory"
            echo "   • git add --dry-run .             # Preview what would be added"
            echo ""
            echo -e "${BLUE}Override: command git add $2${NC} (use with caution)"
            return 1
        fi
    fi

    # Warn on force push
    if [[ "$1" == "push" && ("$2" == "--force" || "$2" == "-f" || "$3" == "--force" || "$3" == "-f") ]]; then
        echo -e "${YELLOW}⚠️  Warning: Force push detected${NC}"
        echo "This will overwrite remote history and can destroy teammates' work!"
        echo ""
        echo -e "Type ${RED}FORCE${NC} to confirm, or use ${GREEN}--force-with-lease${NC} for safer push:"
        read -r confirmation
        if [[ "$confirmation" != "FORCE" ]]; then
            echo -e "${GREEN}✅ Force push cancelled${NC}"
            echo "💡 Try: git push --force-with-lease (safer alternative)"
            return 1
        fi
    fi

    # Warn on dangerous reset
    if [[ "$1" == "reset" && "$2" == "--hard" ]]; then
        echo -e "${YELLOW}⚠️  Warning: Hard reset will destroy uncommitted changes${NC}"
        echo "Type 'RESET' to confirm you want to lose all uncommitted work:"
        read -r confirmation
        if [[ "$confirmation" != "RESET" ]]; then
            echo -e "${GREEN}✅ Reset cancelled${NC}"
            echo "💡 Try: git stash (to save changes temporarily)"
            return 1
        fi
    fi

    # Execute git command
    command git "$@"
}

# ==============================================================================
# DOWNLOAD PROTECTION - Verify before downloading
# ==============================================================================
curl() {
    # Check if downloading a script to execute
    if [[ "$*" == *"| bash"* ]] || [[ "$*" == *"| sh"* ]]; then
        echo -e "${RED}🚫 Blocked: Piping download directly to shell${NC}"
        echo -e "${YELLOW}⚠️  This is extremely dangerous!${NC}"
        echo ""
        echo -e "${GREEN}✅ Safe approach:${NC}"
        echo "   1. Download first: curl -o script.sh <url>"
        echo "   2. Review script:  cat script.sh"
        echo "   3. Then execute:   bash script.sh"
        return 1
    fi

    echo -e "${YELLOW}📥 Download requested with curl${NC}"
    echo -e "URL: ${BLUE}$*${NC}"
    echo ""
    echo -n "Allow download? (y/N): "
    read -r -n 1 reply
    echo
    if [[ ! $reply =~ ^[Yy]$ ]]; then
        echo -e "${RED}✗ Download cancelled${NC}"
        return 1
    fi
    command curl "$@"
}

wget() {
    echo -e "${YELLOW}📥 Download requested with wget${NC}"
    echo -e "URL: ${BLUE}$*${NC}"
    echo ""
    echo -n "Allow download? (y/N): "
    read -r -n 1 reply
    echo
    if [[ ! $reply =~ ^[Yy]$ ]]; then
        echo -e "${RED}✗ Download cancelled${NC}"
        return 1
    fi
    command wget "$@"
}

# ==============================================================================
# RM PROTECTION - Prevent accidental deletions
# ==============================================================================
rm() {
    local force_recursive=false
    local interactive=false
    local args=()
    local targets=()

    # Parse arguments
    for arg in "$@"; do
        case "$arg" in
            -rf|-fr)
                force_recursive=true
                args+=("$arg")
                ;;
            -*r*f*|-*f*r*)
                force_recursive=true
                args+=("$arg")
                ;;
            -*i*)
                interactive=true
                args+=("$arg")
                ;;
            -*)
                args+=("$arg")
                ;;
            *)
                targets+=("$arg")
                ;;
        esac
    done

    # Check for dangerous patterns
    for target in "${targets[@]}"; do
        # Block deletion of home directory
        if [[ "$target" == "$HOME" || "$target" == "~" || "$target" == "/" ]]; then
            echo -e "${RED}🚫 BLOCKED: Attempting to delete critical directory: $target${NC}"
            echo "This would destroy your system!"
            return 1
        fi

        # Warn on .git deletion
        if [[ "$target" == *".git"* ]]; then
            echo -e "${YELLOW}⚠️  Warning: Deleting git directory${NC}"
            echo "This will destroy repository history!"
            echo -n "Type 'DELETE GIT' to confirm: "
            read -r confirmation
            if [[ "$confirmation" != "DELETE GIT" ]]; then
                echo -e "${GREEN}✅ Deletion cancelled${NC}"
                return 1
            fi
        fi
    done

    # If force recursive on non-empty dirs, confirm
    if [[ "$force_recursive" == true && "$interactive" == false ]]; then
        local needs_confirmation=false
        local non_empty_dirs=()

        for target in "${targets[@]}"; do
            if [[ -d "$target" ]]; then
                if [[ -n "$(find "$target" -mindepth 1 -print -quit 2>/dev/null)" ]]; then
                    needs_confirmation=true
                    non_empty_dirs+=("$target")
                fi
            fi
        done

        if [[ "$needs_confirmation" == true ]]; then
            echo -e "${YELLOW}⚠️  WARNING: Permanently deleting non-empty directories:${NC}"
            for dir in "${non_empty_dirs[@]}"; do
                local item_count=$(find "$dir" -mindepth 1 2>/dev/null | wc -l | tr -d ' ')
                echo -e "   📁 ${RED}$dir${NC} (contains ${YELLOW}$item_count${NC} items)"
            done
            echo ""
            echo -e "${RED}🔥 This action cannot be undone!${NC}"
            echo ""
            echo -n "Type 'DELETE ALL' to confirm: "
            read -r confirmation

            if [[ "$confirmation" != "DELETE ALL" ]]; then
                echo -e "${GREEN}✅ Operation cancelled${NC}"
                echo "💡 Try: rm -ri $targets (interactive mode)"
                return 1
            fi
            echo -e "${RED}🗑️  Proceeding with deletion...${NC}"
        fi
    fi

    # Execute rm command
    command rm "${args[@]}" "${targets[@]}"
}

# ==============================================================================
# SHELL PROTECTION STATUS
# ==============================================================================
cursor_protection_status() {
    echo -e "${GREEN}🛡️  Cursor Shell Protection Active${NC}"
    echo ""
    echo "Protected commands:"
    echo "  • git add . / -A        → Blocked (prevents secrets)"
    echo "  • git push --force      → Requires confirmation"
    echo "  • curl/wget             → Requires confirmation"
    echo "  • rm -rf                → Requires confirmation"
    echo ""
    echo -e "${BLUE}Bypass any protection:${NC} command <original-command>"
    echo -e "${YELLOW}Check status:${NC} cursor_protection_status"
}

# Show protection status on source
echo -e "${GREEN}✅ Cursor shell protection loaded${NC}"
echo "Type 'cursor_protection_status' to see protected commands"
