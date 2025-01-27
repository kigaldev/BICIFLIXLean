# =============================
# Configuración básica de Zsh
# =============================

# Agregar rutas importantes al PATH
export PATH="/usr/local/bin:$PATH"
export PATH="/opt/homebrew/bin:$PATH"  # Necesario para sistemas con Apple Silicon (M1/M2)

# =============================
# Configuración de NVM
# =============================

# Configurar NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # Cargar NVM
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # Cargar autocompletado de NVM

# =============================
# Alias útiles (opcional)
# =============================

# Alias para comandos frecuentes
alias ll="ls -lah"  # Listar archivos con detalles
alias gs="git status"  # Atajo para git status
alias ..="cd .."  # Subir un nivel en el directorio

# =============================
# Prompt personalizado (opcional)
# =============================

# Configuración del prompt de Zsh
export PS1="%F{green}%n@%m%f:%F{blue}%~%f %# "

# =============================
# Mejoras de Zsh (opcional)
# =============================

# Activar corrección ortográfica en comandos
setopt correct

# Mostrar el historial al presionar la flecha hacia arriba
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# Activar autocompletado
autoload -Uz compinit
compinit

# =============================
# Final de la configuración
# =============================
