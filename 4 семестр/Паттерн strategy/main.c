#include <stdio.h>
#include <SDL3/SDL.h>

typedef void (*EventHandler)(SDL_Event*);

void handle_mousebuttondown(SDL_Event* event) {
    printf("Клик мыши в (%f, %f)\n", event->button.x, event->button.y);
}

void handle_mousebuttonup(SDL_Event* event) {
    printf("Отпускание кнопки в (%f, %f)\n", event->button.x, event->button.y);
}

void handle_mousewheel(SDL_Event* event) {
    const char* direction = (event->wheel.y > 0) ? "вверх" : "вниз";
    printf("Колёсико %s\n", direction);
}

void handle_mousemotion(SDL_Event* event) {
    printf("Движение мыши в (%f, %f)\n", event->motion.x, event->motion.y);
}

static EventHandler event_handlers[SDL_EVENT_LAST] = {
    [SDL_EVENT_MOUSE_BUTTON_DOWN] = handle_mousebuttondown,
    [SDL_EVENT_MOUSE_BUTTON_UP]   = handle_mousebuttonup,
    [SDL_EVENT_MOUSE_WHEEL]       = handle_mousewheel,
    [SDL_EVENT_MOUSE_MOTION]      = handle_mousemotion
};

void dispatch_event(SDL_Event* event) {
    if (event->type >= 0 && event->type < SDL_EVENT_LAST && event_handlers[event->type]) {
        event_handlers[event->type](event);
    }
}

int main() {
    SDL_Init(SDL_INIT_VIDEO);
    
    SDL_Window* window = SDL_CreateWindow("Strategy in C", 480, 480, SDL_WINDOW_RESIZABLE);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, NULL);
    
    int running = 1;
    while (running) {
        SDL_Event event;
        
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_EVENT_QUIT) {
                running = 0;
            }
            if (event.type == SDL_EVENT_KEY_DOWN && event.key.key == SDLK_ESCAPE) {
                running = 0;
            }
            
            dispatch_event(&event);
        }
        
        SDL_SetRenderDrawColor(renderer, 30, 30, 40, 255);
        SDL_RenderClear(renderer);
        SDL_RenderPresent(renderer);
        
        SDL_Delay(16);
    }
    
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    
    return 0;
}